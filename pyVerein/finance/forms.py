"""
Formmodule for finnaceapp
"""
# Import Forms
from django import forms
# Import localization
from django.utils.translation import ugettext_lazy as _
# Import Accountmodel
from .models import Account, CostCenter, CostObject, Transaction, VirtualAccount

class PersonalAccountCreateForm(forms.ModelForm):
    """
    Formclass for creating debitors & creditors
    """
    class Meta:
        """
        Form metadata
        """
        model = Account
        fields = ('number', 'name')

class PersonalAccountEditForm(forms.ModelForm):
    """
    Formclass for editing debitors & creditors
    """
    class Meta:
        """
        Form metadata
        """
        model = Account
        fields = ('name',)

class ImpersonalAccountCreateForm(forms.ModelForm):
    """
    Formclass for creating impersonal accounts
    """
    class Meta:
        """
        Form metadata
        """
        model = Account
        fields = ('number', 'name', 'account_type')
        widgets = {
            'account_type': forms.RadioSelect(attrs={'class':'mdc-radio__native-control'})
        }
    
    def __init__(self, *args, **kwargs):
        """
        Init form with type choices
        """
        TYPES = (
            (Account.COST, _('Cost')),
            (Account.INCOME, _('Income')),
            (Account.ASSET, _('Asset'))
        )
        super(ImpersonalAccountCreateForm, self).__init__(*args, **kwargs)
        self.fields['account_type'].choices = TYPES

class ImpersonalAccountEditForm(forms.ModelForm):
    """
    Formclass for editing impersonal accounts
    """
    class Meta:
        """
        Form metadata
        """
        model = Account
        fields = ('name', )


class CostCenterCreateForm(forms.ModelForm):
    """
    Formclass for costcenters
    """
    class Meta:
        """
        Form metadata
        """
        model = CostCenter
        fields = ('number', 'name', 'description')

class CostCenterEditForm(forms.ModelForm):
    """
    Formclass for costcenters
    """
    class Meta:
        """
        Form metadata
        """
        model = CostCenter
        fields = ('name', 'description')

class CostObjectCreateForm(forms.ModelForm):
    """
    Formclass for costobjects
    """
    class Meta:
        """
        Form metadata
        """
        model = CostObject
        fields = ('number', 'name', 'description')

class CostObjectEditForm(forms.ModelForm):
    """
    Formclass for costobjects
    """
    class Meta:
        """
        Form metadata
        """
        model = CostObject
        fields = ('name', 'description')

class TransactionCreateForm(forms.ModelForm):
    """
    Formclass for transactions
    """
    class Meta:
        """
        Form metadata
        """
        model = Transaction
        fields = ('account', 'date', 'document_number', 'text', 'debit', 'credit', 'cost_center', 'cost_object')
        localized_fields = ('debit', 'credit')
        widgets = {
            'account': forms.TextInput(),
            'debit': forms.TextInput(),
            'credit': forms.TextInput(),
            'cost_center': forms.TextInput(),
            'cost_object': forms.TextInput(),
        }

class TransactionEditForm(forms.ModelForm):
    """
    Formclass for transactions
    """
    class Meta:
        """
        Form metadata
        """
        model = Transaction
        fields = ('text', 'cost_center', 'cost_object')
        widgets = {
            'cost_center': forms.TextInput(),
            'cost_object': forms.TextInput(),
        }

class VirtualAccountCreateForm(forms.ModelForm):
    """
    Formclass for creating virtual accounts
    """
    class Meta:
        """
        Form metadata
        """
        model = VirtualAccount
        fields = ('number', 'name', 'initial', 'active_from', 'cost_center', 'cost_objects')
        localized_fields = ('initial',)
        widgets = {
            'initial': forms.TextInput(),
            'cost_center': forms.TextInput(),
            'cost_object': forms.TextInput(),
        }
       
class VirtualAccountEditForm(forms.ModelForm):
    """
    Formclass for editing virtual accounts
    """
    class Meta:
        """
        Form metadata
        """
        model = VirtualAccount
        fields = ('name', 'initial', 'active_from', 'cost_center', 'cost_objects')
        localized_fields = ('initial',)
        widgets = {
            'initial': forms.TextInput(),
            'cost_center': forms.TextInput(),
            'cost_object': forms.TextInput(),
        }
