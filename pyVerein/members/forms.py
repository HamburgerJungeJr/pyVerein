from django import forms
from .models import Member


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ('salutation', 'last_name', 'first_name', 'street', 'zipcode', 'city', 'birthday', 'phone', 'mobile', 'fax', 'email', 'membership_number', 'joined_at', 'terminated_at', 'payment_method', 'iban', 'bic', 'debit_mandate_at', 'debit_reference', 'field_1', 'field_2', 'field_3', 'field_4', 'field_5')
        widgets = {
            'salutation': forms.RadioSelect()
        }