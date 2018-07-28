from django import forms
from django.utils.translation import ugettext_lazy as _

class ResetFileInput(forms.widgets.ClearableFileInput):
    template_name = 'utils/clearable_file_input.html'
    clear_checkbox_label = _('Clear')

    def __init__(self, attrs=None, label=None):

        super().__init__(attrs=attrs)
        if label:
            self.clear_checkbox_label = label
        