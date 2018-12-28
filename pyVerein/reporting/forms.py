from django import forms
from .models import Report, Resource
from django.forms.widgets import FileInput


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ('name', 'description', 'report',)
        widgets = {
            'report': FileInput(),
        }

class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ('resource',)