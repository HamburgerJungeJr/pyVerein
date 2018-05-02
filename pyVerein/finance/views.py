"""
Viewmodule for finance app
"""
import datetime
from django.http import JsonResponse
# Import views
from django.views.generic import TemplateView, DetailView, UpdateView, CreateView
# Import forms
from .forms import PersonalAccountCreateForm, PersonalAccountEditForm, ImpersonalAccountCreateForm, ImpersonalAccountEditForm, CostCenterCreateForm, CostCenterEditForm, CostObjectCreateForm, CostObjectEditForm, TransactionCreateForm, TransactionEditForm
# Import reverse.
from django.urls import reverse, reverse_lazy
# Import datatablesview.
from django_datatables_view.base_datatable_view import BaseDatatableView
# Import Q for extended filtering.
from django.db.models import Q, Max, Sum
# Import localization
from django.utils.translation import ugettext_lazy as _
# Import MessageMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.messages import get_messages
# Import Account model
from .models import Account, CostCenter, CostObject, Transaction

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

class CreditorIndexView(LoginRequiredMixin, TemplateView):
    """
    Index view for creditors
    """
    template_name = 'finance/creditor/list.html'

class CreditorCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
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
        # Save object to commit the changes
        self.object.save()
        
        return super(CreditorCreateView, self).form_valid(form)

class CreditorDetailView(LoginRequiredMixin, DetailView):
    """
    Detail view for creditors
    """
    model = Account
    context_object_name = 'creditor'
    template_name = 'finance/creditor/detail.html'

    def get_context_data(self, **kwargs):
        context = super(CreditorDetailView, self).get_context_data(**kwargs)

        context['transactions'] = Transaction.objects.filter(account=self.object.number)

        debit_sum = Transaction.objects.filter(account=self.object.number).aggregate(Sum('debit'))['debit__sum']
        credit_sum = Transaction.objects.filter(account=self.object.number).aggregate(Sum('credit'))['credit__sum']
        context['debit_sum'] = debit_sum if debit_sum else 0
        context['credit_sum'] = credit_sum if credit_sum else 0
        context['saldo'] = (credit_sum if credit_sum else 0) - (debit_sum if debit_sum else 0)

        return context

class CreditorEditView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
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

class CreditorDatatableView(LoginRequiredMixin, BaseDatatableView):
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

class DebitorIndexView(LoginRequiredMixin, TemplateView):
    """
    Index view for debitors
    """
    template_name = 'finance/debitor/list.html'

class DebitorCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
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
        # Save object to commit the changes
        self.object.save()
        
        return super(DebitorCreateView, self).form_valid(form)

class DebitorDetailView(LoginRequiredMixin, DetailView):
    """
    Detail view for debitors
    """
    model = Account
    context_object_name = 'debitor'
    template_name = 'finance/debitor/detail.html'

    def get_context_data(self, **kwargs):
        context = super(DebitorDetailView, self).get_context_data(**kwargs)

        context['transactions'] = Transaction.objects.filter(account=self.object.number)

        debit_sum = Transaction.objects.filter(account=self.object.number).aggregate(Sum('debit'))['debit__sum']
        credit_sum = Transaction.objects.filter(account=self.object.number).aggregate(Sum('credit'))['credit__sum']
        context['debit_sum'] = debit_sum if debit_sum else 0
        context['credit_sum'] = credit_sum if credit_sum else 0
        context['saldo'] = (debit_sum if debit_sum else 0) - (credit_sum if credit_sum else 0)

        return context

class DebitorEditView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
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

class DebitorDatatableView(LoginRequiredMixin, BaseDatatableView):
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

class ImpersonalIndexView(LoginRequiredMixin, TemplateView):
    """
    Index view for impersonal accounts
    """
    template_name = 'finance/impersonal/list.html'

class ImpersonalCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    Create view for impersonal accounts
    """
    model = Account
    context_object_name = 'impersonal'
    template_name = 'finance/impersonal/create.html'
    form_class = ImpersonalAccountCreateForm
    success_message = _('Impersonal account created successfully')

    def get_success_url(self):
        """
        Return detail url as success url
        """
        return reverse_lazy('finance:impersonal_detail', args={self.object.pk})

class ImpersonalDetailView(LoginRequiredMixin, DetailView):
    """
    Detail view for impersonal accounts
    """
    model = Account
    context_object_name = 'impersonal'
    template_name = 'finance/impersonal/detail.html'
    
    def get_context_data(self, **kwargs):
        context = super(ImpersonalDetailView, self).get_context_data(**kwargs)

        context['transactions'] = Transaction.objects.filter(account=self.object.number)

        debit_sum = Transaction.objects.filter(account=self.object.number).aggregate(Sum('debit'))['debit__sum']
        credit_sum = Transaction.objects.filter(account=self.object.number).aggregate(Sum('credit'))['credit__sum']
        context['debit_sum'] = debit_sum if debit_sum else 0
        context['credit_sum'] = credit_sum if credit_sum else 0
        context['saldo'] = (debit_sum if debit_sum else 0) - (credit_sum if credit_sum else 0)

        return context
    
class ImpersonalEditView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Edit view for impersonal accounts
    """
    model = Account
    context_object_name = 'impersonal'
    template_name = 'finance/impersonal/edit.html'
    form_class = ImpersonalAccountEditForm
    success_message = _('Impersonal account saved successfully')

    def get_success_url(self):
        """
        Return detail url as success url
        """
        return reverse_lazy('finance:impersonal_detail', args={self.object.pk})

class ImpersonalDatatableView(LoginRequiredMixin, BaseDatatableView):
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
        return Account.objects.filter(Q(account_type=Account.INCOME) | Q(account_type=Account.COST) | Q(account_type=Account.ASSET))

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

class CostCenterIndexView(LoginRequiredMixin, TemplateView):
    """
    Index view for costcenter
    """
    template_name = 'finance/costcenter/list.html'

class CostCenterCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
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

class CostCenterDetailView(LoginRequiredMixin, DetailView):
    """
    Detail view for costcenter
    """
    model = CostCenter
    context_object_name = 'costcenter'
    template_name = 'finance/costcenter/detail.html'

    def get_context_data(self, **kwargs):
        context = super(CostCenterDetailView, self).get_context_data(**kwargs)

        context['transactions'] = Transaction.objects.filter(cost_center=self.object.number)

        debit_sum = Transaction.objects.filter(cost_center=self.object.number).aggregate(Sum('debit'))['debit__sum']
        credit_sum = Transaction.objects.filter(cost_center=self.object.number).aggregate(Sum('credit'))['credit__sum']
        context['debit_sum'] = debit_sum if debit_sum else 0
        context['credit_sum'] = credit_sum if credit_sum else 0
        context['saldo'] = (credit_sum if credit_sum else 0) - (debit_sum if debit_sum else 0)

        return context

class CostCenterEditView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
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

class CostCenterDatatableView(LoginRequiredMixin, BaseDatatableView):
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

class CostObjectIndexView(LoginRequiredMixin, TemplateView):
    """
    Index view for costobject
    """
    template_name = 'finance/costobject/list.html'

class CostObjectCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
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

class CostObjectDetailView(LoginRequiredMixin, DetailView):
    """
    Detail view for costobject
    """
    model = CostObject
    context_object_name = 'costobject'
    template_name = 'finance/costobject/detail.html'

    def get_context_data(self, **kwargs):
        context = super(CostObjectDetailView, self).get_context_data(**kwargs)

        context['transactions'] = Transaction.objects.filter(cost_object=self.object.number)

        debit_sum = Transaction.objects.filter(cost_object=self.object.number).aggregate(Sum('debit'))['debit__sum']
        credit_sum = Transaction.objects.filter(cost_object=self.object.number).aggregate(Sum('credit'))['credit__sum']
        context['debit_sum'] = debit_sum if debit_sum else 0
        context['credit_sum'] = credit_sum if credit_sum else 0
        context['saldo'] = (credit_sum if credit_sum else 0) - (debit_sum if debit_sum else 0)

        return context

class CostObjectEditView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
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

class CostObjectDatatableView(LoginRequiredMixin, BaseDatatableView):
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

class TransactionIndexView(LoginRequiredMixin, TemplateView):
    """
    Index view for transaction
    """
    template_name = 'finance/transaction/list.html'

class TransactionCreateView(LoginRequiredMixin, CreateView):
    """
    Create view for transaction
    """
    model = Transaction
    context_object_name = 'transaction'
    template_name = 'finance/transaction/create.html'
    form_class = TransactionCreateForm

    def get_success_url(self):
        """
        Return detail url as success url
        """
        debit_sum = Transaction.objects.filter(document_number=self.object.document_number).aggregate(Sum('debit'))['debit__sum']
        credit_sum = Transaction.objects.filter(document_number=self.object.document_number).aggregate(Sum('credit'))['credit__sum']
        if debit_sum != credit_sum:
            return reverse_lazy('finance:transaction_create_continue', args={self.object.document_number})
        else:
            return reverse_lazy('finance:transaction_create')
    
    def form_valid(self, form):
        """
        Set document_number if not set
        """
        # Save validated data
        self.object = form.save(commit = False)
        # Generate document_number
        if self.object.document_number is None:
            max_document_number = Transaction.objects.filter(document_number_generated=True).aggregate(Max('document_number'))['document_number__max']
            next_document_number =  '1' if max_document_number is None else str(int(max_document_number) + 1)[2:]
            self.object.document_number = str(datetime.date.today().strftime('%y')) + next_document_number.zfill(5)
            self.object.document_number_generated = True
        # Save object to commit the changes
        self.object.save()
        
        return super(TransactionCreateView, self).form_valid(form)

class TransactionCreateContinueView(LoginRequiredMixin, CreateView):
    """
    Create view for transaction when first transaction is made
    """
    model = Transaction
    context_object_name = 'transaction'
    template_name = 'finance/transaction/create.html'
    form_class = TransactionCreateForm

    def get_success_url(self):
        """
        Return detail url as success url
        """
        debit_sum = Transaction.objects.filter(document_number=self.object.document_number).aggregate(Sum('debit'))['debit__sum']
        credit_sum = Transaction.objects.filter(document_number=self.object.document_number).aggregate(Sum('credit'))['credit__sum']
        if debit_sum != credit_sum:
            return reverse_lazy('finance:transaction_create_continue', args={self.object.document_number})
        else:
            messages.success(self.request, _('Transaction %s created successfully' % self.object.document_number))
            return reverse_lazy('finance:transaction_create')
    
    def get_initial(self):
        """
        Set initial values from previous document
        """
        initial = super(TransactionCreateContinueView, self).get_initial()
        transaction = Transaction.objects.filter(document_number=self.kwargs['document_number']).first()
        initial['date'] = transaction.date
        initial['document_number'] = transaction.document_number
        initial['text'] = transaction.text

        debit_sum = Transaction.objects.filter(document_number=transaction.document_number).aggregate(Sum('debit'))['debit__sum']
        credit_sum = Transaction.objects.filter(document_number=transaction.document_number).aggregate(Sum('credit'))['credit__sum']

        balance =  (debit_sum if debit_sum is not None else 0) - (credit_sum if credit_sum is not None else 0)
        if balance > 0:
            initial['credit'] = balance
        else:
            initial['debit'] = -balance

        return initial

    def form_valid(self, form):
        """
        Set document_number if not set
        """
        # Save validated data
        self.object = form.save(commit = False)
        # Generate document_number
        if self.object.document_number is None:
            max_document_number = Transaction.objects.filter(document_number_generated=True).aggregate(Max('document_number'))['document_number__max']
            next_document_number =  '1' if max_document_number is None else str(int(max_document_number) + 1)[2:]
            self.object.document_number = str(datetime.date.today().strftime('%y')) + next_document_number.zfill(5)
            self.object.document_number_generated = True
        # Save object to commit the changes
        self.object.save()
        
        return super(TransactionCreateContinueView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        """
        Add transaction with document_number to context
        """
        context = super(TransactionCreateContinueView, self).get_context_data(**kwargs)
        transactions = Transaction.objects.filter(document_number=self.kwargs['document_number'])
        context['transactions'] = transactions

        return context

class TransactionDetailView(LoginRequiredMixin, DetailView):
    """
    Detail view for transaction
    """
    model = Transaction
    context_object_name = 'transaction'
    template_name = 'finance/transaction/detail.html'

class TransactionEditView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Edit view for transaction
    """
    model = Transaction
    context_object_name = 'transaction'
    template_name = 'finance/transaction/edit.html'
    form_class = TransactionEditForm
    success_message = _('Cost object saved successfully')

    def get_success_url(self):
        """
        Return detail url as success url
        """
        return reverse_lazy('finance:transaction_detail', args={self.object.pk})

class TransactionDatatableView(LoginRequiredMixin, BaseDatatableView):
    """
    Datatables.net view for transaction
    """
    # Use Transactionmodel
    model = Transaction

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
                                          'detail_url': reverse('finance:transaction_detail', args=[item.number])})

        # Return data
        return json_data

@login_required
def get_account(request, search):
    if search:
        if search.endswith('%'):
            accounts = Account.objects.filter(Q(number__startswith=search.replace('%', '')) | Q(name__icontains=search))
        else:
            accounts = Account.objects.filter(Q(number=search) | Q(name__icontains=search))
        
        return JsonResponse(createJson(accounts))
    else:
        return JsonResponse({})

@login_required
def get_cost_center(request, search):
    if search:
        if search.endswith('%'):
            cost_centers = CostCenter.objects.filter(Q(number__startswith=search.replace('%', '')) | Q(name__icontains=search))
        else:
            cost_centers = CostCenter.objects.filter(Q(number=search) | Q(name__icontains=search))

        return JsonResponse(createJson(cost_centers))
    else:
        return JsonResponse({})

@login_required
def get_cost_object(request, search):
    if search:
        if search.endswith('%'):
            cost_objects = CostObject.objects.filter(Q(number__startswith=search.replace('%', '')) | Q(name__icontains=search))
        else:
            cost_objects = CostObject.objects.filter(Q(number=search) | Q(name__icontains=search))

        return JsonResponse(createJson(cost_objects))
    else:
        return JsonResponse({})

def createJson(items):
    json_data = {
        'data': []
    }
    for item in items:
        json_data['data'].append({'number': item.number, 'name': item.name})
    
    return json_data
