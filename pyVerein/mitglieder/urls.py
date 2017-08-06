# Import django-urls.
from django.conf.urls import url
# Import views.
from . import views

# Set url-patterns
urlpatterns = [
    url(r'^$', views.index, name='index')
]
