from django.db import models
# Import localization
from django.utils.translation import ugettext_lazy as _

class Account(models.Model):
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

class CostCenter(models.Model):
    """
    Cost center model
    """
    # Cost center number
    number = models.CharField(max_length=10, blank=False, null=False, unique=True, primary_key=True)
    # Cost center name
    name = models.CharField(max_length=255, blank=False, null=False)
    # Description
    description = models.TextField(blank=True, null=True)

class CostObject(models.Model):
    """
    Cost object model
    """
    # Cost object number
    number = models.CharField(max_length=10, blank=False, null=False, unique=True, primary_key=True)
    # Cost object name
    name = models.CharField(max_length=255, blank=False, null=False)
    # Description
    description = models.TextField(blank=True, null=True)

class Transaction(models.Model):
    """
    Transaction model.
    """
    # Account
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='account_transactions')
    # Contra account
    contra_account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='contra_account_transactions')

    # Transaction date
    date = models.DateField(null=False, blank=False)
    # Document number
    document_number = models.CharField(max_length=255, blank=False, null=False)
    # Booking text
    text = models.CharField(max_length=255, blank=False, null=False)

    # Debit value
    debit = models.DecimalField(max_digits=12, decimal_places=2)
    # Credit value
    credit = models.DecimalField(max_digits=12, decimal_places=2)

    # Cost center
    cost_center = models.ForeignKey(CostCenter, on_delete=models.PROTECT)
    # Cost object
    cost_object = models.ForeignKey(CostObject, on_delete=models.PROTECT)

