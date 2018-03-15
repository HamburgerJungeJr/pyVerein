# Import django-admin.
from django.contrib import admin

# Import member model.
from .models import Member

# Register Member in admin.
admin.site.register(Member)
