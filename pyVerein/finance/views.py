"""
Viewmodule for finance app
"""
# Import views
from django.views.generic import TemplateView, DetailView, UpdateView, CreateView
# Import forms
from .forms import PersonalAccountCreateForm, PersonalAccountEditForm, ImpersonalAccountForm, CostCenterCreateForm, CostCenterEditForm, CostObjectCreateForm, CostObjectEditForm
# Import reverse.
from django.urls import reverse, reverse_lazy
# Import datatablesview.
from django_datatables_view.base_datatable_view import BaseDatatableView
# Import Q for extended filtering.
from django.db.models import Q
# Import localization
from django.utils.translation import ugettext_lazy as _
# Import MessageMixin
from django.contrib.messages.views import SuccessMessageMixin
# Import Account model
from .models import Account, CostCenter, CostObject

class CreditorIndexView(TemplateView):
    """
    Index view for creditors
    """
    template_name = 'finance/creditor/list.html'

class CreditorCreateView(SuccessMessageMixin, CreateView):
    """
    Create view for creditors
    """
    model = Account
    context_object_name = 'creditor'
    template_name = 'finance/creditor/create.html'
    form_class = PersonalAccountCreateForm
    success_message = _('Creditor created successfully')

    def get_success_url(self):
        """
        Return detail url as success url
        """
        return reverse_lazy('finance:creditor_detail', args={self.object.pk})

    def form_valid(self, form):
        """
        Update object with account_type
        """
        # Save validated data
        self.object = form.save(commit = False)
        # Set account_type to debitor
        self.object.account_type = Account.CREDITOR
        print(self.object)
        # Save object to commit the changes
        self.object.save()
        
        return super(CreditorCreateView, self).form_valid(form)

class CreditorDetailView(DetailView):
    """
    Detail view for creditors
    """
    model = Account
    context_object_name = 'creditor'
    template_name = 'finance/creditor/detail.html'

class CreditorEditView(SuccessMessageMixin, UpdateView):
    """
    Edit view for creditors
    """
    model = Account
    context_object_name = 'creditor'
    template_name = 'finance/creditor/edit.html'
    form_class = PersonalAccountEditForm
    success_message = _('Creditor saved successfully')

    def get_success_url(self):
        """
        Return detail url as success url
        """
        return reverse_lazy('finance:creditor_detail', args={self.object.pk})

class CreditorDatatableView(BaseDatatableView):
    """
    Datatables.net view for creditors
    """
    # Use Accountmodel
    model = Account

    # Define displayed columns.
    columns = ['number', 'name']

    # Define columns used for ordering.
    order_columns = ['number', 'name']

    # Set maximum returned rows to prevent attacks.
    max_rows = 500

    def get_initial_queryset(self):
        """
        Filter only creditors
        """
        return Account.objects.filter(Q(account_type=Account.CREDITOR))

    def filter_queryset(self, qs):
        """
        Filter rows by given searchterm
        """
        # Read GET parameters.
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(Q(number__icontains=search) | Q(name__icontains=search))

        # Return filtered data.
        return qs

    def prepare_results(self, qs):
        """
        Prepare results to return as dict with urls
        """
        # Initialize data array
        json_data = []

        # Loop through all items in queryset
        for item in qs:
            # Append dictionary with all columns and urls
            json_data.append({'number': item.number, 'name': item.name, 
                                          'detail_url': reverse('finance:creditor_detail', args=[item.number])})

        # Return data
        return json_data

class DebitorIndexView(TemplateView):
    """
    Index view for debitors
    """
    template_name = 'finance/debitor/list.html'

class DebitorCreateView(SuccessMessageMixin, CreateView):
    """
    Create view for debitors
    """
    model = Account
    context_object_name = 'debitor'
    template_name = 'finance/debitor/create.html'
    form_class = PersonalAccountCreateForm
    success_message = _('Debitor created successfully')

    def get_success_url(self):
        """
        Return detail url as success url
        """
        return reverse_lazy('finance:debitor_detail', args={self.object.pk})
    
    def form_valid(self, form):
        """
        Update object with account_type
        """
        # Save validated data
        self.object = form.save(commit = False)
        # Set account_type to debitor
        self.object.account_type = Account.DEBITOR
        print(self.object)
        # Save object to commit the changes
        self.object.save()
        
        return super(DebitorCreateView, self).form_valid(form)

class DebitorDetailView(DetailView):
    """
    Detail view for debitors
    """
    model = Account
    context_object_name = 'debitor'
    template_name = 'finance/debitor/detail.html'

class DebitorEditView(SuccessMessageMixin, UpdateView):
    """
    Edit view for debitors
    """
    model = Account
    context_object_name = 'debitor'
    template_name = 'finance/debitor/edit.html'
    form_class = PersonalAccountEditForm
    success_message = _('Debitor saved successfully')

    def get_success_url(self):
        """
        Return detail url as success url
        """
        return reverse_lazy('finance:debitor_detail', args={self.object.pk})

class DebitorDatatableView(BaseDatatableView):
    """
    Datatables.net view for debitors
    """
    # Use Accountmodel
    model = Account

    # Define displayed columns.
    columns = ['number', 'name']

    # Define columns used for ordering.
    order_columns = ['number', 'name']

    # Set maximum returned rows to prevent attacks.
    max_rows = 500

    def get_initial_queryset(self):
        """
        Fiter only debitors
        """
        return Account.objects.filter(Q(account_type=Account.DEBITOR))

    def filter_queryset(self, qs):
        """
        Filter rows by giver searchterm
        """
        # Read GET parameters.
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(Q(number__icontains=search) | Q(name__icontains=search))

        # Return filtered data.
        return qs

    def prepare_results(self, qs):
        """
        Prepare results to return as dict with urls
        """
        # Initialize data array
        json_data = []

        # Loop through all items in queryset
        for item in qs:
            # Append dictionary with all columns and urls
            json_data.append({'number': item.number, 'name': item.name, 
                                          'detail_url': reverse('finance:debitor_detail', args=[item.number])})

        # Return data
        return json_data

class ImpersonalIndexView(TemplateView):
    """
    Index view for impersonal accounts
    """
    template_name = 'finance/impersonal/list.html'

class ImpersonalCreateView(SuccessMessageMixin, CreateView):
    """
    Create view for impersonal accounts
    """
    model = Account
    context_object_name = 'impersonal'
    template_name = 'finance/impersonal/create.html'
    form_class = ImpersonalAccountForm
    success_message = _('Impersonal account created successfully')

    def get_success_url(self):
        """
        Return detail url as success url
        """
        return reverse_lazy('finance:impersonal_detail', args={self.object.pk})

class ImpersonalDetailView(DetailView):
    """
    Detail view for impersonal accounts
    """
    model = Account
    context_object_name = 'impersonal'
    template_name = 'finance/impersonal/detail.html'

class ImpersonalEditView(SuccessMessageMixin, UpdateView):
    """
    Edit view for impersonal accounts
    """
    model = Account
    context_object_name = 'impersonal'
    template_name = 'finance/impersonal/edit.html'
    form_class = ImpersonalAccountForm
    success_message = _('Impersonal account saved successfully')

    def get_success_url(self):
        """
        Return detail url as success url
        """
        return reverse_lazy('finance:impersonal_detail', args={self.object.pk})

class ImpersonalDatatableView(BaseDatatableView):
    """
    Datatables.net view for impersonal accounts
    """
    # Use Accountmodel
    model = Account

    # Define displayed columns.
    columns = ['number', 'name']

    # Define columns used for ordering.
    order_columns = ['number', 'name']

    # Set maximum returned rows to prevent attacks.
    max_rows = 500

    def get_initial_queryset(self):
        """
        Filter only impersonal accounts
        """
        return Account.objects.filter(Q(account_type=Account.INCOME) | Q(account_type=Account.COST))

    def filter_queryset(self, qs):
        """
        Filter rows by given searchterm
        """
        # Read GET parameters.
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(Q(number__icontains=search) | Q(name__icontains=search))

        # Return filtered data.
        return qs

    def prepare_results(self, qs):
        """
        Prepare results to return as dict with urls
        """
        # Initialize data array
        json_data = []

        # Loop through all items in queryset
        for item in qs:
            # Append dictionary with all columns and urls
            json_data.append({'number': item.number, 'name': item.name, 
                                          'detail_url': reverse('finance:impersonal_detail', args=[item.number])})

        # Return data
        return json_data

class CostCenterIndexView(TemplateView):
    """
    Index view for costcenter
    """
    template_name = 'finance/costcenter/list.html'

class CostCenterCreateView(SuccessMessageMixin, CreateView):
    """
    Create view for costcenter
    """
    model = CostCenter
    context_object_name = 'costcenter'
    template_name = 'finance/costcenter/create.html'
    form_class = CostCenterCreateForm
    success_message = _('Cost center created successfully')

    def get_success_url(self):
        """
        Return detail url as success url
        """
        return reverse_lazy('finance:costcenter_detail', args={self.object.pk})

class CostCenterDetailView(DetailView):
    """
    Detail view for costcenter
    """
    model = CostCenter
    context_object_name = 'costcenter'
    template_name = 'finance/costcenter/detail.html'

class CostCenterEditView(SuccessMessageMixin, UpdateView):
    """
    Edit view for costcenter
    """
    model = CostCenter
    context_object_name = 'costcenter'
    template_name = 'finance/costcenter/edit.html'
    form_class = CostCenterEditForm
    success_message = _('Cost center saved successfully')

    def get_success_url(self):
        """
        Return detail url as success url
        """
        return reverse_lazy('finance:costcenter_detail', args={self.object.pk})

class CostCenterDatatableView(BaseDatatableView):
    """
    Datatables.net view for costcenter
    """
    # Use CostCentermodel
    model = CostCenter

    # Define displayed columns.
    columns = ['number', 'name']

    # Define columns used for ordering.
    order_columns = ['number', 'name']

    # Set maximum returned rows to prevent attacks.
    max_rows = 500

    def filter_queryset(self, qs):
        """
        Filter rows by given searchterm
        """
        # Read GET parameters.
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(Q(number__icontains=search) | Q(name__icontains=search))

        # Return filtered data.
        return qs

    def prepare_results(self, qs):
        """
        Prepare results to return as dict with urls
        """
        # Initialize data array
        json_data = []

        # Loop through all items in queryset
        for item in qs:
            # Append dictionary with all columns and urls
            json_data.append({'number': item.number, 'name': item.name, 
                                          'detail_url': reverse('finance:costcenter_detail', args=[item.number])})

        # Return data
        return json_data


class CostObjectIndexView(TemplateView):
    """
    Index view for costobject
    """
    template_name = 'finance/costobject/list.html'

class CostObjectCreateView(SuccessMessageMixin, CreateView):
    """
    Create view for costobject
    """
    model = CostObject
    context_object_name = 'costobject'
    template_name = 'finance/costobject/create.html'
    form_class = CostObjectCreateForm
    success_message = _('Cost object created successfully')

    def get_success_url(self):
        """
        Return detail url as success url
        """
        return reverse_lazy('finance:costobject_detail', args={self.object.pk})

class CostObjectDetailView(DetailView):
    """
    Detail view for costobject
    """
    model = CostObject
    context_object_name = 'costobject'
    template_name = 'finance/costobject/detail.html'

class CostObjectEditView(SuccessMessageMixin, UpdateView):
    """
    Edit view for costobject
    """
    model = CostObject
    context_object_name = 'costobject'
    template_name = 'finance/costobject/edit.html'
    form_class = CostObjectEditForm
    success_message = _('Cost object saved successfully')

    def get_success_url(self):
        """
        Return detail url as success url
        """
        return reverse_lazy('finance:costobject_detail', args={self.object.pk})

class CostObjectDatatableView(BaseDatatableView):
    """
    Datatables.net view for costobject
    """
    # Use CostObjectmodel
    model = CostObject

    # Define displayed columns.
    columns = ['number', 'name']

    # Define columns used for ordering.
    order_columns = ['number', 'name']

    # Set maximum returned rows to prevent attacks.
    max_rows = 500

    def filter_queryset(self, qs):
        """
        Filter rows by given searchterm
        """
        # Read GET parameters.
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(Q(number__icontains=search) | Q(name__icontains=search))

        # Return filtered data.
        return qs

    def prepare_results(self, qs):
        """
        Prepare results to return as dict with urls
        """
        # Initialize data array
        json_data = []

        # Loop through all items in queryset
        for item in qs:
            # Append dictionary with all columns and urls
            json_data.append({'number': item.number, 'name': item.name, 
                                          'detail_url': reverse('finance:costobject_detail', args=[item.number])})

        # Return data
        return json_data
