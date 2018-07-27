"""
Module for definition of user-related models.
"""
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    Extended user to store the avatar.
    """

    avatar = models.FileField(null=True, blank=True, default=None)
