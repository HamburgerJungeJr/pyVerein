"""
Formmodule for finnaceapp
"""
# Import Forms
from django import forms
# Import localization
from django.utils.translation import ugettext_lazy as _
# Import Accountmodel
from .models import Account

class PersonalAccountCreateForm(forms.ModelForm):
    """
    Formclass for creating debitors & creditors
    """
    class Meta:
        """
        Form metadata
        """
        model = Account
        fields = ('number', 'name', 'account_type')
        widgets = {
            'account_type': forms.RadioSelect()
        }

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

class ImpersonalAccountForm(forms.ModelForm):
    """
    Formclass for impersonal accounts
    """
    class Meta:
        """
        Form metadata
        """
        model = Account
        fields = ('number', 'name', 'account_type')
        widgets = {
            'account_type': forms.RadioSelect()
        }
    
    def __init__(self, *args, **kwargs):
        """
        Init form with type choices
        """
        TYPES = (
            (Account.COST, _('Cost')),
            (Account.INCOME, _('Income'))
        )
        super(ImpersonalAccountForm, self).__init__(*args, **kwargs)
        self.fields['account_type'].choices = TYPES