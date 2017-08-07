# Import django render shortcut.
from django.shortcuts import render, get_object_or_404 as get
# Import members.
from .models import Member
# Import datatablesview.
from django_datatables_view.base_datatable_view import BaseDatatableView
# Import Q for extended filtering.
from django.db.models import Q

# Index-View.
def index(request):
    # Set Context.
    context = {}

    # Return rendered template.
    return render(request, 'members/index.html', context)

# Detail-View.
def detail(request, member_id):
    # Get member.
    member = get(Member, pk=member_id)

    # Return rendered template.
    return render(request, 'members/detail.html', {'member': member})

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
    def filter_request(self, qs):
        # Read GET parameters.
        GET = self.request.GET
        if(search):
            qs = qs.filter(Q(last_name__icontains=search) | Q(first_name__icontains=search) | Q(street__icontains=search) | Q(zipcode__icontains=search) | Q(city__icontains=search))

        # Return filtered data.
        return qs
