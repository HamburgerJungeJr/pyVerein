# Import django render shortcut.
from django.shortcuts import render, get_object_or_404 as get
# Import reverse.
from django.urls import reverse, reverse_lazy
# Import members.
from django.views.generic import TemplateView, DetailView, UpdateView, CreateView

from .models import Member
# Import datatablesview.
from django_datatables_view.base_datatable_view import BaseDatatableView
# Import Q for extended filtering.
from django.db.models import Q
# Import ajax helper
from utils.views import render_ajax
# Import localization
from django.utils.translation import ugettext_lazy as _


# Index-View.
class MemberIndexView(TemplateView):
    template_name = 'members/member_list.html'


# Detail-View.
class MemberDetailView(DetailView):
    model = Member
    context_object_name = 'member'


# Edit-View.
class MemberEditView(UpdateView):
    model = Member
    fields = ['first_name']
    context_object_name = 'member'
    template_name = 'members/member_edit.html'

    def get_success_url(self):
        return reverse_lazy('members:detail', args={self.object.pk})


# Edit-View.
class MemberCreateView(CreateView):
    model = Member
    fields = ['first_name']
    context_object_name = 'member'
    template_name = 'members/member_create.html'

    def get_success_url(self):
        return reverse_lazy('members:detail', args={self.object.pk})


# Datatable api view.
class MemberDatatableView(BaseDatatableView):
    # Use Membermodel
    model = Member

    # Define displayed columns.
    columns = ['last_name', 'first_name', 'street', 'zipcode', 'city']

    # Define columns used for ordering.
    order_columns = ['last_name', 'first_name', 'street', 'zipcode', 'city']

    # Set maximum returned rows to prevent attacks.
    max_rows = 500

    # Filter rows.
    def filter_queryset(self, qs):
        # Read GET parameters.
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(
                Q(last_name__icontains=search) | Q(first_name__icontains=search) | Q(street__icontains=search) | Q(
                    zipcode__icontains=search) | Q(city__icontains=search))

        # Return filtered data.
        return qs

    # Prepare results to return as dict with urls
    def prepare_results(self, qs):
        # Initialize data array
        json_data = []

        # Loop through all items in queryset
        for item in qs:
            # Append dictionary with all columns and urls
            json_data.append({'last_name': item.last_name, 'first_name': item.first_name, 'street': item.street,
                              'zipcode': item.zipcode, 'city': item.city,
                              'detail_url': reverse('members:detail', args=[item.id])})

        # Return data
        return json_data
