from django import forms
from .models import Account
# Import localization
from django.utils.translation import ugettext_lazy as _

class AccountCreateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('number', 'name', 'account_type')
        widgets = {
            'account_type': forms.RadioSelect()
        }

class AccountEditForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('name',)

class ImpersonalAccountForm(forms.ModelForm):
    class Meta:
        
        model = Account
        fields = ('number', 'name', 'account_type')
        widgets = {
            'account_type': forms.RadioSelect()
        }
    
    def __init__(self, *args, **kwargs):
        TYPES = (
            (Account.COST, _('Cost')),
            (Account.INCOME, _('Income'))
        )
        super(ImpersonalAccountForm, self).__init__(*args, **kwargs)
        self.fields['account_type'].choices = TYPES