from django.db import models

#Member model.
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
    birthday = models.DateField(blank=True)
