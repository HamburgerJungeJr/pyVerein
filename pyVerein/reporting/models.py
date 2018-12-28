from django.db import models
from author.decorators import with_author
from utils.models import ModelBase
from django.utils.translation import ugettext_lazy as _
from django.forms import ValidationError

class Report(ModelBase):
    """
    Model for storing reports
    """

    name = models.CharField(null=False, blank=False, max_length=255)
    
    description = models.TextField(null=True, blank=True)

    report = models.FileField(null=True, blank=True, upload_to='reports/definition')
        
    def clean(self, *args, **kwargs):
        super(Report, self).clean(*args, **kwargs)
        if not self.report:
            raise ValidationError(_('Report must not be empty'))

def get_resource_path(instance, filename):
    """
    Return resourcepath with report id folder
    """
    return "reports/resource/{}/{}".format(instance.report.id, filename)

class Resource(ModelBase):
    """
    Model for report-resource
    """
    report = models.ForeignKey(Report, on_delete=models.CASCADE)

    resource = models.FileField(null=False, blank=False, upload_to=get_resource_path)

