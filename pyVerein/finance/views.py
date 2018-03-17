from django.shortcuts import render
from .models import Account
from django.views.generic import TemplateView, DetailView, UpdateView, CreateView
from .forms import AccountCreateForm, AccountEditForm, ImpersonalAccountForm
# Import reverse.
from django.urls import reverse, reverse_lazy
# Import datatablesview.
from django_datatables_view.base_datatable_view import BaseDatatableView
# Import Q for extended filtering.
from django.db.models import Q

# Index-View.
class CreditorIndexView(TemplateView):
    template_name = 'finance/creditor_list.html'

# Detail-View.
class CreditorDetailView(DetailView):
    model = Account
    context_object_name = 'creditor'
    template_name = 'finance/creditor_detail.html'

# Edit-View.
class CreditorEditView(UpdateView):
    model = Account
    context_object_name = 'creditor'
    template_name = 'finance/creditor_edit.html'
    form_class = AccountEditForm

    def get_success_url(self):
        return reverse_lazy('finance:creditor_detail', args={self.object.pk})


# Edit-View.
class CreditorCreateView(CreateView):
    model = Account
    context_object_name = 'creditor'
    template_name = 'finance/creditor_create.html'
    form_class = AccountCreateForm

    def get_success_url(self):
        return reverse_lazy('finance:creditor_detail', args={self.object.pk})

# Datatable api view.
class CreditorDatatableView(BaseDatatableView):
    # Use Accountmodel
    model = Account

    # Define displayed columns.
    columns = ['number', 'name']

    # Define columns used for ordering.
    order_columns = ['number', 'name']

    # Set maximum returned rows to prevent attacks.
    max_rows = 500

    def get_initial_queryset(self):
        # Filter only creditors
        return Account.objects.filter(Q(account_type=Account.CREDITOR))

    # Filter rows.
    def filter_queryset(self, qs):
        # Read GET parameters.
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(Q(number__icontains=search) | Q(name__icontains=search))

        # Return filtered data.
        return qs

    # Prepare results to return as dict with urls
    def prepare_results(self, qs):
        # Initialize data array
        json_data = []

        # Loop through all items in queryset
        for item in qs:
            # Append dictionary with all columns and urls
            json_data.append({'number': item.number, 'name': item.name, 
                                          'detail_url': reverse('finance:creditor_detail', args=[item.number])})

        # Return data
        return json_data

# Index-View.
class DebitorIndexView(TemplateView):
    template_name = 'finance/debitor_list.html'

# Detail-View.
class DebitorDetailView(DetailView):
    model = Account
    context_object_name = 'debitor'
    template_name = 'finance/debitor_detail.html'

# Edit-View.
class DebitorEditView(UpdateView):
    model = Account
    context_object_name = 'debitor'
    template_name = 'finance/debitor_edit.html'
    form_class = AccountEditForm

    def get_success_url(self):
        return reverse_lazy('finance:debitor_detail', args={self.object.pk})


# Edit-View.
class DebitorCreateView(CreateView):
    model = Account
    context_object_name = 'debitor'
    template_name = 'finance/debitor_create.html'
    form_class = AccountCreateForm

    def get_success_url(self):
        return reverse_lazy('finance:debitor_detail', args={self.object.pk})

# Datatable api view.
class DebitorDatatableView(BaseDatatableView):
    # Use Accountmodel
    model = Account

    # Define displayed columns.
    columns = ['number', 'name']

    # Define columns used for ordering.
    order_columns = ['number', 'name']

    # Set maximum returned rows to prevent attacks.
    max_rows = 500

    def get_initial_queryset(self):
        # Filter only debitors
        return Account.objects.filter(Q(account_type=Account.DEBITOR))

    # Filter rows.
    def filter_queryset(self, qs):
        # Read GET parameters.
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(Q(number__icontains=search) | Q(name__icontains=search))

        # Return filtered data.
        return qs

    # Prepare results to return as dict with urls
    def prepare_results(self, qs):
        # Initialize data array
        json_data = []

        # Loop through all items in queryset
        for item in qs:
            # Append dictionary with all columns and urls
            json_data.append({'number': item.number, 'name': item.name, 
                                          'detail_url': reverse('finance:debitor_detail', args=[item.number])})

        # Return data
        return json_data

# Index-View.
class ImpersonalIndexView(TemplateView):
    template_name = 'finance/impersonal_list.html'

# Detail-View.
class ImpersonalDetailView(DetailView):
    model = Account
    context_object_name = 'impersonal'
    template_name = 'finance/impersonal_detail.html'

# Edit-View.
class ImpersonalEditView(UpdateView):
    model = Account
    context_object_name = 'impersonal'
    template_name = 'finance/impersonal_edit.html'
    form_class = ImpersonalAccountForm

    def get_success_url(self):
        return reverse_lazy('finance:impersonal_detail', args={self.object.pk})


# Edit-View.
class ImpersonalCreateView(CreateView):
    model = Account
    context_object_name = 'impersonal'
    template_name = 'finance/impersonal_create.html'
    form_class = ImpersonalAccountForm

    def get_success_url(self):
        return reverse_lazy('finance:impersonal_detail', args={self.object.pk})

# Datatable api view.
class ImpersonalDatatableView(BaseDatatableView):
    # Use Accountmodel
    model = Account

    # Define displayed columns.
    columns = ['number', 'name']

    # Define columns used for ordering.
    order_columns = ['number', 'name']

    # Set maximum returned rows to prevent attacks.
    max_rows = 500

    def get_initial_queryset(self):
        # Filter only impersonal accounts
        return Account.objects.filter(Q(account_type=Account.INCOME) | Q(account_type=Account.COST))

    # Filter rows.
    def filter_queryset(self, qs):
        # Read GET parameters.
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(Q(number__icontains=search) | Q(name__icontains=search))

        # Return filtered data.
        return qs

    # Prepare results to return as dict with urls
    def prepare_results(self, qs):
        # Initialize data array
        json_data = []

        # Loop through all items in queryset
        for item in qs:
            # Append dictionary with all columns and urls
            json_data.append({'number': item.number, 'name': item.name, 
                                          'detail_url': reverse('finance:impersonal_detail', args=[item.number])})

        # Return data
        return json_data
