from django.db import models
from django.contrib.auth.models import Group
from account.models import User

class ModelBase(models.Model):
    class Meta:
        abstract = True

    # Created at
    created_at = models.DateTimeField(auto_now_add=True)
    # Modified at
    modified_at = models.DateTimeField(auto_now=True)

class AccessRestrictedModel(models.Model):
    class Meta:
        abstract = True
    
    user = models.ManyToManyField(User, blank=True)
    groups = models.ManyToManyField(Group, blank=True)

    def is_access_granted(self, user):
        """
        Checks if object has no access restriction or if user is allowed to view the object. 
        Either direct or by one of his groups.
        """

        # No access restriction
        if not self.user.all().exists() and not self.groups.all().exists():
            return True
        
        # User is admin
        if user.is_superuser:
            return True

        # Direct access granted for user
        if user in self.user.all():
            return True
        
        # Check if user is in one of the granted groups
        user_groups = user.groups.all()
        for group in self.groups.all():
            if group in user_groups:
                return True
        
        # No access granted for user
        return False