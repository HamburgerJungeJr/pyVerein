from django import forms
from .models import Report, Resource
from django.forms.widgets import FileInput, CheckboxSelectMultiple
from django.utils.translation import ugettext_lazy as _
class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ('name', 'description', 'report', 'model', 'jsonql_query', 'user', 'groups')
        widgets = {
            'report': FileInput(),
            'model': CheckboxSelectMultiple(attrs={'class': 'mdc-checkbox__native-control'}),
            'user': CheckboxSelectMultiple(attrs={'class': 'mdc-checkbox__native-control'}),
            'groups': CheckboxSelectMultiple(attrs={'class': 'mdc-checkbox__native-control'})
        }

class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ('resource',)