from django.db import models
from author.decorators import with_author
from utils.models import ModelBase, AccessRestrictedModel
from django.utils.translation import ugettext_lazy as _
from django.forms import ValidationError
import uuid
from separatedvaluesfield.models import SeparatedValuesField
from author.decorators import with_author

def get_report_path(instance, filename):
    """
    Return reportpath with report id folder
    """
    return "protected/reports/{}/definition/{}".format(instance.uuid, filename)

@with_author
class Report(ModelBase, AccessRestrictedModel):
    """
    Model for storing reports
    """

    class Meta:
        permissions = (
            ('run_report', 'Can run report'),
            ('download_data', 'Can download data'),
            ('download_member_data', 'Can download member data'),
            ('download_division_data', 'Can download division data'),
            ('download_subscription_data', 'Can download subscription data'),
            ('download_account_data', 'Can download account data'),
            ('download_costcenter_data', 'Can download costcenter data'),
            ('download_costobject_data', 'Can download costobject data'),
            ('download_transaction_data', 'Can download transaction data'),
            ('download_closuretransaction_data', 'Can download closuretransaction data'),
            ('download_closurebalance_data', 'Can download closurebalance data'),
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

    jsonql_query = models.TextField(null=False, blank=False)

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

@with_author
class Resource(ModelBase):
    """
    Model for report-resource
    """
    report = models.ForeignKey(Report, on_delete=models.CASCADE)

    resource = models.FileField(null=False, blank=False, upload_to=get_resource_path)

