# Import django-urls.
from django.urls import path
# Import views.
from . import views

# Set app name
app_name = 'app'
# Set url-patterns
urlpatterns = [
    path('', views.index, name='index'),
]
