from django.db import models

# Member model.
class Member(models.Model):
    # Lastname
    last_name = models.CharField(max_length=50)
    # Firstname
    first_name = models.CharField(max_length=50)
    # Street
    street = models.CharField(blank=True, max_length=200)
    # Zipcode
    zipcode = models.CharField(blank=True, max_length=10)
    # City
    city = models.CharField(blank=True, max_length=100)
    # Birthday
    birthday = models.DateField(blank=True, null=True)

    # Return full name
    def get_full_name(self):
        return '{0} {1}'.format(self.first_name, self.last_name)

    # Return full name as string representation
    def __str__(self):
        return self.get_full_name()
