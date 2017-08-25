from django.db import models

# Member model.
class Member(models.Model):
    # Choices for salutation
    MR = 'MR'
    MRS = 'MRS'
    SALUTATIONS = (
        (MR, 'Mr.'),
        (MRS, 'Mrs.')
    )
    # Salutation
    salutation = models.CharField(choices=SALUTATIONS, max_length=3, default=MR)
    # Lastname
    last_name = models.CharField(max_length=50)
    # Firstname
    first_name = models.CharField(max_length=50)

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

    # Choices for payment method
    CASH = 'CA'
    REMITTANCE = 'RE'
    DEBIT = 'DE'
    PAYMENT_METHODS = (
        (CASH, 'Cash'),
        (REMITTANCE, 'Remittance'),
        (DEBIT, 'Direct Debit')
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
        return self.terminated_at is not None

    # Return full name as string representation
    def __str__(self):
        return self.get_full_name()
