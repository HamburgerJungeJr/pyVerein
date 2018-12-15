from django.db import models
# Import localization
from django.utils.translation import ugettext_lazy as _
from author.decorators import with_author
from django.db.models import Q

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
    class Meta:
        permissions = (
            ('view_creditor', "Can view creditor"),
            ('add_creditor', "Can add creditor"),
            ('change_creditor', "Can change creditor"),
            ('view_debitor', "Can view debitor"),
            ('add_debitor', "Can add debitor"),
            ('change_debitor', "Can change debitor"),
            ('view_impersonal', "Can view impersonal"),
            ('add_impersonal', "Can add impersonal"),
            ('change_impersonal', "Can change impersonal"),
        )

    # Choices for account type
    CREDITOR = 'CRE'
    DEBITOR = 'DEB'
    COST = 'COS'
    INCOME = 'INC'
    ASSET = 'ASS'
    ACCOUNT_TYPES = (
        (CREDITOR, _('Creditor')),
        (DEBITOR, _('Debitor')),
        (COST, _('Cost')),
        (INCOME, _('Income')),
        (ASSET, _('Asset'))
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
    # Internal number to keep connection of transactions
    internal_number = models.IntegerField(null=False, blank=False, default=0)
    # Is transaction reset
    reset = models.BooleanField(blank=False, null=False, default=False)
    # Clearing Number
    clearing_number = models.IntegerField(null=True, blank=True)
    # Accounting year
    accounting_year = models.IntegerField(blank=True, null=True)

    def is_cleared(self):
        """
        Returns whether the transaction was cleared
        """
        for transaction in Transaction.objects.filter((Q(account__account_type=Account.DEBITOR) | Q(account__account_type=Account.CREDITOR)) & Q(internal_number=self.internal_number)):
            if not transaction.clearing_number:
                return False

        return True

@with_author
class ClosureTransaction(ModelBase):
    """
    Transaction model for annual closure.
    """
    # Account number
    account_number = models.CharField(max_length=10, blank=False, null=False)
    # Account name
    account_name = models.CharField(max_length=255, blank=False, null=False)

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

    # Cost center number
    cost_center_number = models.CharField(max_length=10, blank=True, null=True)
    # Cost center name
    cost_center_name = models.CharField(max_length=255, blank=True, null=True)
    # Description
    cost_center_description = models.TextField(blank=True, null=True)

    # Cost object number
    cost_object_number = models.CharField(max_length=10, blank=True, null=True)
    # Cost object name
    cost_object_name = models.CharField(max_length=255, blank=True, null=True)
    # Description
    cost_object_description = models.TextField(blank=True, null=True)

    # Is document_number generated
    document_number_generated = models.BooleanField(default=False)
    # Internal number to keep connection of transactions
    internal_number = models.IntegerField(null=False, blank=False, default=0)
    # Is transaction reset
    reset = models.BooleanField(blank=False, null=False, default=False)
    # Clearing Number
    clearing_number = models.IntegerField(null=True, blank=True)
    # Accounting year
    accounting_year = models.IntegerField(blank=True, null=True)

@with_author
class ClosureBalance(ModelBase):
    """
    Model for balances at closure
    """

    # Closure year
    year = models.IntegerField(blank=True, null=True, unique=True)

    # Claims at end of year
    claims = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    # Liabilities at end of year
    liabilities = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

