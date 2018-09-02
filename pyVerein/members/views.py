# Import django render shortcut.
from django.shortcuts import render, get_object_or_404 as get
# Import reverse.
from django.urls import reverse, reverse_lazy
# Import members.
from django.views.generic import TemplateView, DetailView, UpdateView, CreateView
# Import Member.
from .forms import MemberForm, DivisionForm
from .models import Member, Division
# Import datatablesview.
from django_datatables_view.base_datatable_view import BaseDatatableView
# Import Q for extended filtering.
from django.db.models import Q

# Import localization
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

# Index-View.
class MemberIndexView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = 'members.view_member'
    template_name = 'members/member_list.html'


# Detail-View.
class MemberDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'members.view_member'
    model = Member
    context_object_name = 'member'


# Edit-View.
class MemberEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'members.change_member'
    model = Member
    context_object_name = 'member'
    template_name = 'members/member_edit.html'
    form_class = MemberForm

    def get_success_url(self):
        return reverse_lazy('members:detail', args={self.object.pk})


# Edit-View.
class MemberCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'members.add_member'
    model = Member
    context_object_name = 'member'
    template_name = 'members/member_create.html'
    form_class = MemberForm

    def get_success_url(self):
        return reverse_lazy('members:detail', args={self.object.pk})


# Datatable api view.
class MemberDatatableView(LoginRequiredMixin, PermissionRequiredMixin, BaseDatatableView):
    permission_required = 'members.view_member'
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

# Index-View.
class DivisionIndexView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = 'members.view_division'
    template_name = 'members/division_list.html'


# Detail-View.
class DivisionDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'members.view_division'
    model = Division
    context_object_name = 'division'

    def get_context_data(self, **kwargs):
        context = super(DivisionDetailView, self).get_context_data(**kwargs)

        context['members'] = Member.objects.filter(division=self.object.pk)

        return context

# Edit-View.
class DivisionEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'members.change_division'
    model = Division
    context_object_name = 'division'
    template_name = 'members/division_edit.html'
    form_class = DivisionForm

    def get_success_url(self):
        return reverse_lazy('members:division_detail', args={self.object.pk})


# Edit-View.
class DivisionCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'members.add_division'
    model = Division
    context_object_name = 'division'
    template_name = 'members/division_create.html'
    form_class = DivisionForm

    def get_success_url(self):
        return reverse_lazy('members:division_detail', args={self.object.pk})


# Datatable api view.
class DivisionDatatableView(LoginRequiredMixin, PermissionRequiredMixin, BaseDatatableView):
    permission_required = 'members.view_division'
    # Use Divisionmodel
    model = Division

    # Define displayed columns.
    columns = ['name']

    # Define columns used for ordering.
    order_columns = ['name']

    # Set maximum returned rows to prevent attacks.
    max_rows = 500

    # Filter rows.
    def filter_queryset(self, qs):
        # Read GET parameters.
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(
                Q(name__icontains=search))

        # Return filtered data.
        return qs

    # Prepare results to return as dict with urls
    def prepare_results(self, qs):
        # Initialize data array
        json_data = []

        # Loop through all items in queryset
        for item in qs:
            # Append dictionary with all columns and urls
            json_data.append({'name': item.name, 'count': Member.objects.filter(division=self.pk).count(),
                              'detail_url': reverse('members:division_detail', args=[item.id])})

        # Return data
        return json_data
