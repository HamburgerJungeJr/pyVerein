# Import django-admin.
from django.contrib import admin

# Import member model.
from .models import Report

# Register report in admin.
admin.site.register(Report)
