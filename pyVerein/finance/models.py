from django.db import models
# Import localization
from django.utils.translation import ugettext_lazy as _
from author.decorators import with_author

class ModelBase(models.Model):
    class Meta:
        abstract = True

    # Created at
    created_at = models.DateTimeField(auto_now_add=True)
    # Modified at
    modified_at = models.DateTimeField(auto_now=True)

@with_author
class Account(ModelBase):
    """
    Account model.
    """
    # Choices for account type
    CREDITOR = 'CRE'
    DEBITOR = 'DEB'
    COST = 'COS'
    INCOME = 'INC'
    ACCOUNT_TYPES = (
        (CREDITOR, _('Creditor')),
        (DEBITOR, _('Debitor')),
        (COST, _('Cost')),
        (INCOME, _('Income'))
    )
    # Account number
    number = models.CharField(max_length=10, blank=False, null=False, unique=True, primary_key=True)
    # Account name
    name = models.CharField(max_length=255, blank=False, null=False)
    # Account type: debitor/creditor/cost/income
    account_type = models.CharField(blank=False, null=False, choices=ACCOUNT_TYPES, max_length=3, default=COST)

@with_author
class CostCenter(ModelBase):
    """
    Cost center model
    """
    # Cost center number
    number = models.CharField(max_length=10, blank=False, null=False, unique=True, primary_key=True)
    # Cost center name
    name = models.CharField(max_length=255, blank=False, null=False)
    # Description
    description = models.TextField(blank=True, null=True)

@with_author
class CostObject(ModelBase):
    """
    Cost object model
    """
    # Cost object number
    number = models.CharField(max_length=10, blank=False, null=False, unique=True, primary_key=True)
    # Cost object name
    name = models.CharField(max_length=255, blank=False, null=False)
    # Description
    description = models.TextField(blank=True, null=True)

@with_author
class Transaction(ModelBase):
    """
    Transaction model.
    """
    # Account
    account = models.ForeignKey(Account, on_delete=models.PROTECT)

    # Transaction date
    date = models.DateField(null=False, blank=False)
    # Document number
    document_number = models.CharField(max_length=255, blank=True, null=True)
    # Transaction text
    text = models.CharField(max_length=255, blank=False, null=False)

    # Debit value
    debit = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    # Credit value
    credit = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    # Cost center
    cost_center = models.ForeignKey(CostCenter, on_delete=models.PROTECT, blank=True, null=True)
    # Cost object
    cost_object = models.ForeignKey(CostObject, on_delete=models.PROTECT, blank=True, null=True)

    # Is document_number generated
    document_number_generated = models.BooleanField(default=False)