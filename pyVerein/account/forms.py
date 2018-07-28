from django import forms
from .models import User
from utils.widgets import ResetFileInput
from django.utils.translation import ugettext_lazy as _

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'avatar')

        widgets = {
            'avatar': ResetFileInput(label=_('Reset profile image')),
        }