from django import forms
from .models import Member, Division, Subscription
from django.forms.widgets import TextInput, CheckboxSelectMultiple

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ('salutation', 'last_name', 'first_name', 'street', 'zipcode', 'city', 'birthday', 'phone', 'mobile', 'fax', 'email', 'membership_number', 'division', 'joined_at', 'terminated_at', 'payment_method', 'subscription', 'iban', 'bic', 'debit_mandate_at', 'debit_reference', 'field_1', 'field_2', 'field_3', 'field_4', 'field_5')
        widgets = {
            'salutation': forms.RadioSelect(attrs={'class':'mdc-radio__native-control'}),
            'subscription': forms.CheckboxSelectMultiple(attrs={'class': 'mdc-checkbox__native-control'}),
            'division': forms.CheckboxSelectMultiple(attrs={'class': 'mdc-checkbox__native-control'}),
        }

class DivisionForm(forms.ModelForm):
    class Meta:
        model = Division
        fields = ('name', 'user', 'groups')
        widgets = {
            'user': CheckboxSelectMultiple(attrs={'class': 'mdc-checkbox__native-control'}),
            'groups': CheckboxSelectMultiple(attrs={'class': 'mdc-checkbox__native-control'})
        }

class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ('name', 'amount', 'payment_frequency', 'income_account', 'debitor_account', 'cost_center', 'cost_object',)
        widgets = {
            'amount': forms.TextInput(),
            'income_account': TextInput(),
            'debitor_account': TextInput(),
            'cost_center': TextInput(),
            'cost_object': TextInput(),
            'payment_frequency': forms.RadioSelect(attrs={'class':'mdc-radio__native-control'})
        }