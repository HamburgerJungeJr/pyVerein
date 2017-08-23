# Import django render shortcut.
from django.shortcuts import render, get_object_or_404 as get
# Import reverse.
from django.urls import reverse
# Import members.
from .models import Member
# Import datatablesview.
from django_datatables_view.base_datatable_view import BaseDatatableView
# Import Q for extended filtering.
from django.db.models import Q
# Import DetailView
from django.views.generic.detail import DetailView


# Index-View.
def index(request):
    # Set Context.
    context = {}

    # Return rendered template.
    return render(request, 'members/index.html', context)


# Detail-View.
class MemberDetailView(DetailView):
    model = Member

# Datatable api view.
class DatatableAPI(BaseDatatableView):
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
