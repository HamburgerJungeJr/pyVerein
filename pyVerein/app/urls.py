# Import django-urls.
from django.conf.urls import url
# Import views.
from . import views

# Set app name
app_name = 'app'
# Set url-patterns
urlpatterns = [
    url(r'^$', views.index, name='index'),
]
