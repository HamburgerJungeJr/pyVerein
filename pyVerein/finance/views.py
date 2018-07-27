"""
Viewmodule for finance app
"""
import datetime
from django.http import JsonResponse, HttpResponseRedirect
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
from decimal import Decimal
import random
import string
from dynamic_preferences.registries import global_preferences_registry

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

    def get_context_data(self, **kwargs):
        context = super(TransactionCreateView, self).get_context_data(**kwargs)
    
        # Session_id for destinguishing multiple parallel transactions
        session_id = self.kwargs.get('session_id', None)
        if not session_id:
            session_id = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
        context['session_id'] = session_id

        context['transactions'] = self.request.session.get(session_id + 'transactions')
        step = self.kwargs.get('step', None)
        if step:
            context['save_url'] = reverse_lazy('finance:transaction_create_step', kwargs={'step':step, 'session_id':session_id})
        else:
            context['save_url'] = reverse_lazy('finance:transaction_create_session', kwargs={'session_id':session_id})
        return context

    def get_initial(self):
        """
        Set initial values from previous document
        """
        initial = super(TransactionCreateView, self).get_initial()
        session_id = self.kwargs.get('session_id', '')
        transactions = self.request.session.get(session_id + 'transactions')
        step = self.kwargs.get('step', None)
        if step and transactions:
            initial['account'] = transactions[step]['account'] 
            initial['date'] = transactions[step]['date']
            initial['document_number'] = transactions[step]['document_number']
            initial['text'] = transactions[step]['text']
            initial['debit'] = transactions[step]['debit']
            initial['credit'] = transactions[step]['credit']
            initial['cost_center'] = transactions[step]['cost_center']
            initial['cost_object'] = transactions[step]['cost_object']
        else:
            if transactions is not None:
                initial['date'] = transactions['0']['date']
                initial['document_number'] = transactions['0']['document_number']
                initial['text'] = transactions['0']['text']

                debit_sum = Decimal(0)
                credit_sum = Decimal(0)
                for transaction in transactions.values():
                    debit_sum += Decimal(transaction['debit'] if transaction['debit'] is not None else 0)
                    credit_sum += Decimal(transaction['credit'] if transaction['credit'] is not None else 0)

                balance =  debit_sum - credit_sum
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

        session_id = self.kwargs.get('session_id', '')

        # Generate document_number
        if self.object.document_number is None:
            max_document_number = Transaction.objects.filter(document_number_generated=True).aggregate(Max('document_number'))['document_number__max']
            next_document_number =  '1' if max_document_number is None else str(int(max_document_number) + 1)[2:]
            self.object.document_number = str(datetime.date.today().strftime('%y')) + next_document_number.zfill(5)
            self.object.document_number_generated = True
        # Save object to commit the changes
        #self.object.save()

        # Save object to session
        transactions = self.request.session.get(session_id + 'transactions')
        if (transactions is None):
            transactions = {
                0: {
                    'account':  str(self.object.account.number) if self.object.account is not None else None,
                    'date':  self.object.date.strftime('%d.%m.%Y'),
                    'document_number': self.object.document_number,
                    'text':  self.object.text,
                    'debit':  str(self.object.debit) if self.object.debit is not None else None,
                    'credit':  str(self.object.credit) if self.object.credit is not None else None,
                    'cost_center':  str(self.object.cost_center.number) if self.object.cost_center is not None else None,
                    'cost_object':  str(self.object.cost_object.number) if self.object.cost_object is not None else None,
                    'document_number_generated':  str(self.object.document_number_generated)
                }
            }
            self.request.session[session_id + 'transactions'] = transactions
        else:
            key = None
            step = self.kwargs.get('step', None)
            if step:
                key = step
            else:
                key = str(int(max(transactions.keys())) + 1)
            transactions[key] = {
                'account':  str(self.object.account.number) if self.object.account is not None else None,
                'date':  self.object.date.strftime('%d.%m.%Y'),
                'document_number': self.object.document_number,
                'text':  self.object.text,
                'debit':  str(self.object.debit) if self.object.debit is not None else None,
                'credit':  str(self.object.credit) if self.object.credit is not None else None,
                'cost_center':  str(self.object.cost_center.number) if self.object.cost_center is not None else None,
                'cost_object':  str(self.object.cost_object.number) if self.object.cost_object is not None else None,
                'document_number_generated':  str(transactions['0']['document_number_generated'])
            }

            debit_sum = Decimal(0)
            credit_sum = Decimal(0)
            for transaction in transactions.values():
                # Sums
                debit_sum += Decimal(transaction['debit'] if transaction['debit'] is not None else 0)
                credit_sum += Decimal(transaction['credit'] if transaction['credit'] is not None else 0)

                # Ckeck if document number is altered, then update#
                if transaction['document_number'] != self.object.document_number:
                    transaction['document_number'] = self.object.document_number
            
            if debit_sum != credit_sum:
                self.request.session[session_id + 'transactions'] = transactions
            else:
                # Get last internal_number
                internal_number = Transaction.objects.all().aggregate(Max('internal_number'))['internal_number__max'] + 1
                # Save transactions from session to db
                for transaction in transactions.values():
                    obj = Transaction()
                    obj.account = Account.objects.get(number=transaction['account'])
                    obj.date = datetime.datetime.strptime(transaction['date'], '%d.%m.%Y')
                    obj.document_number = transaction['document_number']
                    obj.text = transaction['text']
                    obj.debit = Decimal(transaction['debit']) if transaction['debit'] is not None else None
                    obj.credit = Decimal(transaction['credit']) if transaction['credit'] is not None else None
                    obj.cost_center = CostCenter.objects.get(number=transaction['cost_center']) if transaction['cost_center'] is not None else None
                    obj.cost_object = CostObject.objects.get(number=transaction['cost_object']) if transaction['cost_object'] is not None else None
                    obj.document_number_generated = transaction['document_number_generated']
                    obj.internal_number = internal_number
                    obj.save()
                messages.success(self.request, _('Transaction {0:s} saved successfully').format(transactions['0']['document_number']))
                # Clear session
                del self.request.session[session_id + 'transactions']
                return HttpResponseRedirect(reverse_lazy('finance:transaction_create'))

        return HttpResponseRedirect(reverse_lazy('finance:transaction_create_session', kwargs={'session_id':session_id}))

class TransactionDetailView(LoginRequiredMixin, TemplateView):
    """
    Detail view for transaction
    """
    model = Transaction
    template_name = 'finance/transaction/detail.html'

    def get_context_data(self, **kwargs):
        context = super(TransactionDetailView, self).get_context_data(**kwargs)
        
        transactions = Transaction.objects.filter(internal_number=kwargs['internal_number'])
        context['transactions'] = transactions
        context['date'] = transactions[0].date
        context['document_number'] = transactions[0].document_number
        context['internal_number'] = transactions[0].internal_number

        return context

class TransactionEditView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Edit view for transaction
    """
    model = Transaction
    template_name = 'finance/transaction/edit.html'
    form_class = TransactionEditForm
    context_object_name = 'transaction'
    
    def get_context_data(self, **kwargs):
        context = super(TransactionEditView, self).get_context_data(**kwargs)

        internal_number = self.kwargs.get('internal_number', None)
        context['internal_number'] = internal_number
        context['transactions'] = Transaction.objects.filter(internal_number=internal_number)
        return context

    def get_success_url(self):
        internal_number = self.kwargs.get('internal_number', '')
        pk = self.kwargs.get('pk', None)
        return reverse_lazy('finance:transaction_edit', kwargs={'internal_number':internal_number, 'pk':pk})

    def get_success_message(self, cleaned_data):
        return _('Receipt {0:s} updated successfully').format(str(self.object.document_number))
 
class TransactionDatatableView(LoginRequiredMixin, BaseDatatableView):
    """
    Datatables.net view for transaction
    """
    # Use Transactionmodel
    model = Transaction

    # Define displayed columns.
    columns = ['date','document_number',  'account', 'text', 'debit', 'credit', 'cost_center', 'cost_object']

    # Define columns used for ordering.
    order_columns = ['date', 'document_number', 'account', 'text', 'debit', 'credit', 'cost_center', 'cost_object']

    # Set maximum returned rows to prevent attacks.
    max_rows = 500

    def filter_queryset(self, qs):
        """
        Filter rows by given searchterm
        """
        # Read GET parameters.
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(
                Q(document_number__icontains=search) | 
                Q(account__number__icontains=search) | 
                Q(text__icontains=search) | 
                Q(cost_center__number__icontains=search) | 
                Q(cost_object__number__icontains=search)
            )

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
            # Retrieve accounttype
            account_url = None
            if item.account.account_type == Account.DEBITOR: 
                account_url = reverse('finance:debitor_detail', args=[item.account.number])
            if item.account.account_type == Account.CREDITOR: 
                account_url = reverse('finance:creditor_detail', args=[item.account.number])
            if item.account.account_type == Account.COST or item.account.account_type == Account.INCOME or item.account.account_type == Account.ASSET: 
                account_url = reverse('finance:impersonal_detail', args=[item.account.number])

            # Append dictionary with all columns and urls
            json_data.append({
                'document_number': item.document_number, 
                'date': item.date.strftime('%d.%m.%Y'), 
                'account': item.account.number, 
                'text': item.text, 
                'debit': item.debit, 
                'credit': item.credit, 
                'cost_center': item.cost_center.number if item.cost_center is not None else '', 
                'cost_object': item.cost_object.number if item.cost_object is not None else '', 
                'transaction_url': reverse('finance:transaction_detail', args=[item.internal_number]),
                'account_url': account_url,
                'cost_center_url': reverse('finance:costcenter_detail', args=[item.cost_center.number]) if item.cost_center is not None else '',
                'cost_object_url': reverse('finance:costobject_detail', args=[item.cost_object.number]) if item.cost_object is not None else ''
            })

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

@login_required
def reset_transaction(request, internal_number):
    transactions = Transaction.objects.filter(Q(internal_number=internal_number) & Q(reset=False))
    internal_number = None

    if not transactions:
        messages.error(request, _('Receipt already reset'))
        return HttpResponseRedirect(reverse_lazy('finance:transaction_list'))
    else:
        # Get last internal_number
        internal_number = Transaction.objects.all().aggregate(Max('internal_number'))['internal_number__max'] + 1
    for transaction in transactions:
        transaction.reset = True
        transaction.save()

        reset_new_transaction = transaction
        reset_new_transaction.pk = None

        global_preferences = global_preferences_registry.manager()
        reset_new_transaction.document_number = global_preferences['Finance__reset_prefix'] + transaction.document_number

        reset_new_transaction.debit, reset_new_transaction.credit = transaction.credit, transaction.debit
        reset_new_transaction.reset = True
        reset_new_transaction.internal_number = internal_number
        
        reset_new_transaction.save()
    
    messages.success(request, _('Receipt reset successfully'))
    return HttpResponseRedirect(reverse_lazy('finance:transaction_list'))

@login_required
def reset_new_transaction(request, internal_number):
    transactions = Transaction.objects.filter(Q(internal_number=internal_number) & Q(reset=False))
    internal_number = None

    # Create session id   
    session_id = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
    session_transactions = {}

    if not transactions:
        messages.error(request, _('Receipt already reset'))
        return HttpResponseRedirect(reverse_lazy('finance:transaction_list'))
    else:
        # Get last internal_number
        internal_number = Transaction.objects.all().aggregate(Max('internal_number'))['internal_number__max'] + 1
    for key, transaction in enumerate(transactions):
        # Add transaction to session data
        session_transactions[key] = {
            'account':  str(transaction.account.number) if transaction.account is not None else None,
            'date':  transaction.date.strftime('%d.%m.%Y'),
            'document_number': transaction.document_number,
            'text':  transaction.text,
            'debit':  str(transaction.debit) if transaction.debit is not None else None,
            'credit':  str(transaction.credit) if transaction.credit is not None else None,
            'cost_center':  str(transaction.cost_center.number) if transaction.cost_center is not None else None,
            'cost_object':  str(transaction.cost_object.number) if transaction.cost_object is not None else None,
            'document_number_generated':  str(transaction.document_number_generated)
        }
        transaction.reset = True
        transaction.save()

        reset_new_transaction = transaction
        reset_new_transaction.pk = None

        global_preferences = global_preferences_registry.manager()
        reset_new_transaction.document_number = global_preferences['Finance__reset_prefix'] + transaction.document_number

        reset_new_transaction.debit, reset_new_transaction.credit = transaction.credit, transaction.debit
        reset_new_transaction.reset = True
        reset_new_transaction.internal_number = internal_number
        
        reset_new_transaction.save()

    # Save transactions to session
    request.session[session_id + 'transactions'] = session_transactions

    messages.success(request, _('Receipt reset successfully'))
    return HttpResponseRedirect(reverse_lazy('finance:transaction_create_step', kwargs={'session_id':session_id, 'step': 0}))