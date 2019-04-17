"""
Module for definition of user-related models.
"""
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

class CaseInsensitiveUserManager(UserManager):
    def get_by_natural_key(self, username):
        case_insensitive_username_field = '{}__iexact'.format(self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_username_field: username})

class User(AbstractUser):
    """
    Extended user to store the avatar.
    """
    objects = CaseInsensitiveUserManager()
    avatar = models.ImageField(null=True, blank=True, default=None, upload_to='user')
