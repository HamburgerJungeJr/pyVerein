"""
Viewmodule for finance app
"""
import datetime
from django.http import JsonResponse
# Import views
from django.views.generic import TemplateView, DetailView, UpdateView, CreateView
# Import forms
from .forms import PersonalAccountCreateForm, PersonalAccountEditForm, ImpersonalAccountForm, CostCenterCreateForm, CostCenterEditForm, CostObjectCreateForm, CostObjectEditForm, TransactionCreateForm, TransactionEditForm
# Import reverse.
from django.urls import reverse, reverse_lazy
# Import datatablesview.
from django_datatables_view.base_datatable_view import BaseDatatableView
# Import Q for extended filtering.
from django.db.models import Q, Max, Sum
# Import localization
from django.utils.translation import ugettext_lazy as _
# Import MessageMixin
from django.contrib.messages.views import SuccessMessageMixin
# Import Account model
from .models import Account, CostCenter, CostObject, Transaction
# Import Wizrad for Transactions
from formtools.wizard.views import SessionWizardView
from formtools.wizard.forms import ManagementForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.exceptions import ValidationError

from decimal import *

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

    def get_context_data(self, **kwargs):
        context = super(DebitorDetailView, self).get_context_data(**kwargs)

        transactions = Transaction.objects.filter(account == self.kwargs['pk'])
        context['transactions'] = transactions

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

class TransactionIndexView(TemplateView):
    """
    Index view for transaction
    """
    template_name = 'finance/transaction/list.html'

class TransactionWizard(SessionWizardView):
    form_list = [TransactionCreateForm]

    template_name = 'finance/transaction/create.html'

    post_data = {}

    def done(self, form_list, **kwargs):
        try:
            # Set document_number if not set
            # Save validated data
            document_number = None
            document_number_generated = False
            if self.post_data['0']['document_number'] is None:
                max_document_number = Transaction.objects.filter(document_number_generated=True).aggregate(Max('document_number'))['document_number__max']
                next_document_number =  '1' if max_document_number is None else str(int(max_document_number) + 1)[2:]
                document_number = str(datetime.date.today().strftime('%y')) + next_document_number.zfill(5)
                document_number_generated = True
            # Create transactions from forms
            for key in self.post_data:
                document_number = document_number if document_number else self.post_data[key]['document_number']

                transaction = Transaction()
                transaction.account = self.post_data[key]['account']
                transaction.date = self.post_data[key]['date']
                transaction.document_number = document_number
                transaction.text = self.post_data[key]['text']
                transaction.debit = self.post_data[key]['debit']
                transaction.credit = self.post_data[key]['credit']
                transaction.cost_center = self.post_data[key]['cost_center']
                transaction.cost_object = self.post_data[key]['cost_object']
                transaction.document_number_generated = document_number_generated
                transaction.save()

            messages.success(self.request, _('Transaction %s created successfully' % document_number))
            self.instance_dict = None
            self.storage.reset()
            self.storage.current_step = self.steps.first
            return HttpResponseRedirect(reverse_lazy('finance:transaction_create'))
        except ValueError as e:
            form_list[-1].add_error(None, e)
            return self.render(form_list[-1])
        

    def post(self, *args, **kwargs):
        """
        This method handles POST requests.
        The wizard will render either the current step (if form validation
        wasn't successful), the next step (if the current step was stored
        successful) or the done view (if no more steps are available)
        """
        # Look for a wizard_goto_step element in the posted data which
        # contains a valid step name. If one was found, render the requested
        # form. (This makes stepping back a lot easier).
        wizard_goto_step = self.request.POST.get('wizard_goto_step', None)
        if wizard_goto_step and wizard_goto_step in self.get_form_list():
            return self.render_goto_step(wizard_goto_step)
        # Check if form was refreshed
        management_form = ManagementForm(self.request.POST, prefix=self.prefix)
        if not management_form.is_valid():
            raise ValidationError(
                _('ManagementForm data is missing or has been tampered.'),
                code='missing_management_form',
            )
        form_current_step = management_form.cleaned_data['current_step']
        if (form_current_step != self.steps.current and
                self.storage.current_step is not None):
            # form refreshed, change current step
            self.storage.current_step = form_current_step

        # get the form for the current step
        form = self.get_form(data=self.request.POST, files=self.request.FILES)

        # and try to validate
        if form.is_valid():
        # if the form is valid, store the cleaned data and files.
            self.storage.set_step_data(self.steps.current, self.process_step(form))
            self.storage.set_step_files(self.steps.current, self.process_step_files(form))

            # Save form data to post_data
            self.post_data.update({
                self.steps.current: 
                    {
                        'account': form.cleaned_data['account'],
                        'date': form.cleaned_data['date'],
                        'document_number': form.cleaned_data['document_number'],
                        'text': form.cleaned_data['text'],
                        'debit': form.cleaned_data['debit'],
                        'credit': form.cleaned_data['credit'],
                        'cost_center': form.cleaned_data['cost_center'],
                        'cost_object': form.cleaned_data['cost_object']
                    }
            })

            # Check if debit=credit. If not render new form, otherwise finish wizard
            debit = Decimal(0)
            credit = Decimal(0)
            #for step in self.form_list:
            for key in self.post_data:
                #data = self.get_cleaned_data_for_step(step)
                if self.post_data[key]['debit'] is not None:
                    debit += Decimal(self.post_data[key]['debit'])
                if self.post_data[key]['credit'] is not None:
                    credit += Decimal(self.post_data[key]['credit'])
            
            if debit != credit:
                next_step = str(int(self.steps.current) + 1)

                # Get inital data
                #data = self.get_cleaned_data_for_step(self.steps.first)
                
                initial_data = {
                    'date': self.post_data['0']['date'],
                    'text': self.post_data['0']['text'],
                    'document_number': self.post_data['0']['document_number']
                }

                balance =  debit - credit
                if balance > 0:
                    initial_data.update({'credit': balance})
                else:
                    initial_data.update({'debit': -balance})

                # Add to initial_dict
                #self.initial_dict.update({next_step: initial_data})

                if len(self.form_list) <= int(self.steps.current) + 1:
                    self.form_list.update({next_step: TransactionCreateForm})
                
                new_form = TransactionCreateForm(next_step,
                    data=self.storage.get_step_data(next_step),
                    files=self.storage.get_step_files(next_step),
                    initial=initial_data)
                # change the stored current step
                self.storage.current_step = next_step
                return self.render(new_form, **kwargs)
            else:
                # no more steps, render done view
                return self.render_done(form, **kwargs)
        return self.render(form)

class TransactionDetailView(DetailView):
    """
    Detail view for transaction
    """
    model = Transaction
    context_object_name = 'transaction'
    template_name = 'finance/transaction/detail.html'

class TransactionEditView(SuccessMessageMixin, UpdateView):
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

class TransactionDatatableView(BaseDatatableView):
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

def get_account(request, search):
    if search:
        if search.endswith('%'):
            accounts = Account.objects.filter(Q(number__startswith=search.replace('%', '')) | Q(name__icontains=search))
        else:
            accounts = Account.objects.filter(Q(number=search) | Q(name__icontains=search))
        
        return JsonResponse(createJson(accounts))
    else:
        return JsonResponse({})

def get_cost_center(request, search):
    if search:
        if search.endswith('%'):
            cost_centers = CostCenter.objects.filter(Q(number__startswith=search.replace('%', '')) | Q(name__icontains=search))
        else:
            cost_centers = CostCenter.objects.filter(Q(number=search) | Q(name__icontains=search))

        return JsonResponse(createJson(cost_centers))
    else:
        return JsonResponse({})

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