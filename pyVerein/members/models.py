from django.db import models
# Import localization
from django.utils.translation import ugettext_lazy as _
# Import datetime
from datetime import datetime
from finance.models import Account, CostCenter, CostObject
from dynamic_preferences.registries import global_preferences_registry
from utils.models import AccessRestrictedModel

# Member model.
class Member(models.Model):
    class Meta:
        permissions = ( 
            ('view_field_salutation', 'Can view field salutation'),
            ('view_field_last_name', 'Can view field last_name'),
            ('view_field_first_name', 'Can view field first_name'),
            ('view_field_street', 'Can view field street'),
            ('view_field_zipcode', 'Can view field zipcode'),
            ('view_field_city', 'Can view field city'),
            ('view_field_birthday', 'Can view field birthday'),
            ('view_field_phone', 'Can view field phone'),
            ('view_field_mobile', 'Can view field mobile'),
            ('view_field_fax', 'Can view field fax'),
            ('view_field_email', 'Can view field email'),
            ('view_field_membership_number', 'Can view field membership number'),
            ('view_field_joined_at', 'Can view field joined at'),
            ('view_field_terminated_at', 'Can view field terminated at'),
            ('view_field_division', 'Can view field division'),
            ('view_field_payment_method', 'Can view field payment method'),
            ('view_field_iban', 'Can view field iban'),
            ('view_field_bic', 'Can view field bic'),
            ('view_field_debit_mandate_at', 'Can view field debit mandate at'),
            ('view_field_debit_reference', 'Can view field debit reference'),
            ('view_field_subscription', 'Can view field subscription'),
            ('view_field_field_1', 'Can view field field 1'),
            ('view_field_field_2', 'Can view field field 2'),
            ('view_field_field_3', 'Can view field field 3'),
            ('view_field_field_4', 'Can view field field 4'),
            ('view_field_field_5', 'Can view field field 5'),
        )

    # Choices for salutation
    MR = 'MR'
    MRS = 'MRS'
    SALUTATIONS = (
        (MR, _('Mr.')),
        (MRS, _('Mrs.'))
    )
    # Salutation
    salutation = models.CharField(blank=False, null=False, choices=SALUTATIONS, max_length=3, default=MR)
    # Lastname
    last_name = models.CharField(blank=False, null=False, max_length=50)
    # Firstname
    first_name = models.CharField(blank=False, null=False, max_length=50)

    # Street
    street = models.CharField(blank=True, null=True, max_length=200)
    # Zipcode
    zipcode = models.CharField(blank=True, null=True, max_length=10)
    # City
    city = models.CharField(blank=True, null=True, max_length=100)

    # Birthday
    birthday = models.DateField(blank=True, null=True)

    # Phone
    phone = models.CharField(blank=True, null=True, max_length=20)
    # mobile
    mobile = models.CharField(blank=True, null=True, max_length=20)
    # fax
    fax = models.CharField(blank=True, null=True, max_length=20)
    # email
    email = models.CharField(blank=True, null=True, max_length=255)

    # Membership number
    membership_number = models.CharField(blank=True, null=True, max_length=100)
    # Joined at
    joined_at = models.DateField(blank=True, null=True)
    # Terminated at
    terminated_at = models.DateField(blank=True, null=True)
    # Division
    division = models.ForeignKey('Division', on_delete=models.PROTECT, blank=True, null=True)

    # Choices for payment method
    CASH = 'CA'
    REMITTANCE = 'RE'
    DEBIT = 'DE'
    PAYMENT_METHODS = (
        (CASH, _('Cash')),
        (REMITTANCE, _('Remittance')),
        (DEBIT, _('Direct Debit'))
    )
    # Payment method
    payment_method = models.CharField(choices=PAYMENT_METHODS, max_length=2, default=DEBIT)
    # IBAN
    iban = models.CharField(blank=True, null=True, max_length=34)
    # BIC
    bic = models.CharField(blank=True, null=True, max_length=11)
    # Direct debit mandate granted at
    debit_mandate_at = models.DateField(blank=True, null=True)
    # Direct debit reference
    debit_reference = models.CharField(blank=True, null=True, max_length=100)
    # Subscription
    subscription = models.ManyToManyField('Subscription', blank=True)

    # Additional field 1
    field_1 = models.CharField(blank=True, null=True, max_length=255)
    # Additional field 2
    field_2 = models.CharField(blank=True, null=True, max_length=255)
    # Additional field 3
    field_3 = models.CharField(blank=True, null=True, max_length=255)
    # Additional field 4
    field_4 = models.CharField(blank=True, null=True, max_length=255)
    # Additional field 5
    field_5 = models.CharField(blank=True, null=True, max_length=255)


    # Return full name
    def get_full_name(self):
        return '{0} {1}'.format(self.first_name, self.last_name)

    # Return true if membership is terminated
    def is_terminated(self):
        if self.terminated_at is not None:
            return self.terminated_at <= datetime.now().date()
        else:
            return False

    # Return full name as string representation
    def __str__(self):
        return self.get_full_name()

class Division(AccessRestrictedModel):
    """
    Division model
    """

    # Name
    name = models.CharField(blank=False, null=False, max_length=255)
    income_account = models.ForeignKey(Account, blank=True, null=True, on_delete=models.PROTECT, related_name='+')
    debitor_account = models.ForeignKey(Account, blank=True, null=True, on_delete=models.PROTECT, related_name='+')
    cost_center = models.ForeignKey(CostCenter, blank=True, null=True, on_delete=models.PROTECT, related_name='+')
    cost_object = models.ForeignKey(CostObject, blank=True, null=True, on_delete=models.PROTECT, related_name='+')

    def __str__(self):
        return self.name

    def get_income_account(self):
        """
        Returns the assigned income account, if set, otherwise the global default
        """
        if self.income_account:
            return self.income_account
        else:
            global_preferences = global_preferences_registry.manager()
            return CostCenter.objects.get(pk=global_preferences['Members__division_income_account'])
            
    def get_debitor_account(self):
        """
        Returns the assigned debitor account, if set, otherwise the global default
        """
        if self.debitor_account:
            return self.debitor_account
        else:
            global_preferences = global_preferences_registry.manager()
            return CostCenter.objects.get(pk=global_preferences['Members__division_debitor_account'])

    def get_cost_center(self):
        """
        Returns the assigned cost center, if set, otherwise the global default
        """
        if self.cost_center:
            return self.cost_center
        else:
            global_preferences = global_preferences_registry.manager()
            return CostCenter.objects.get(pk=global_preferences['Members__division_cost_center'])

    def get_cost_object(self):
        """
        Returns the assigned cost object, if set, otherwise the global default
        """
        if self.cost_object:
            return self.cost_object
        else:
            global_preferences = global_preferences_registry.manager()
            return CostCenter.objects.get(pk=global_preferences['Members__division_cost_object'])

class Subscription(models.Model):
    """
    Subscription model
    """

    MONTHLY = 'MON'
    QUARTERLY = 'QUA'
    HALFYEARLY = 'HAL'
    YEARLY = 'YEA'
    PAYMENT_FREQUENCY = (
        (MONTHLY, _('Monthly')),
        (QUARTERLY, _('Quarterly')),
        (HALFYEARLY, _('Half-Yearly')),
        (YEARLY, _('Yearly'))
    )

    # Name
    name = models.CharField(blank=False, null=False, max_length=255)
    # Amount
    amount = models.DecimalField(blank=False, null=False, max_digits=12, decimal_places=2)
    # Payment frequency
    payment_frequency = models.CharField(choices=PAYMENT_FREQUENCY, max_length=3, default=YEARLY)

    def __str__(self):
        return self.name