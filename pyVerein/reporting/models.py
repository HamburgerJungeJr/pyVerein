from django.db import models
from author.decorators import with_author
from utils.models import ModelBase
from django.utils.translation import ugettext_lazy as _
from django.forms import ValidationError
import uuid
from separatedvaluesfield.models import SeparatedValuesField

def get_report_path(instance, filename):
    """
    Return reportpath with report id folder
    """
    return "protected/reports/{}/definition/{}".format(instance.uuid, filename)

class Report(ModelBase):
    """
    Model for storing reports
    """

    class Meta:
        permissions = (
            ('run_report', 'Can run report'),
        )

    MEMBER = 'MEM'
    DIVISION = 'DIV'
    SUBSCRIPTION = 'SUB'
    ACCOUNT = 'ACC'
    COSTCENTER = 'COC'
    COSTOBJECT = 'COO'
    TRANSACTION = 'TRA'
    CLOSURETRANSACTION = 'CTR'
    CLOSUREBALANCE = 'CBA'

    MODELS = (
        (MEMBER, _('Member')),
        (DIVISION, _('Division')),
        (SUBSCRIPTION, _('Subscription')),
        (ACCOUNT, _('Account')),
        (COSTCENTER, _('Costcenter')),
        (COSTOBJECT, _('Costobject')),
        (TRANSACTION, _('Transaction')),
        (CLOSURETRANSACTION, _('Closuretransaction')),
        (CLOSUREBALANCE, _('Closurebalance'))
    )

    name = models.CharField(null=False, blank=False, max_length=255)
    
    description = models.TextField(null=True, blank=True)

    report = models.FileField(null=True, blank=True, upload_to=get_report_path)

    model = SeparatedValuesField(null=False, blank=False, max_length=255, choices=MODELS, default=[MEMBER])

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
        
    def clean(self, *args, **kwargs):
        super(Report, self).clean(*args, **kwargs)
        if not self.report:
            raise ValidationError(_('Report must not be empty'))

def get_resource_path(instance, filename):
    """
    Return resourcepath with report id folder
    """
    return "protected/reports/{}/resource/{}".format(instance.report.uuid, filename)

class Resource(ModelBase):
    """
    Model for report-resource
    """
    report = models.ForeignKey(Report, on_delete=models.CASCADE)

    resource = models.FileField(null=False, blank=False, upload_to=get_resource_path)

