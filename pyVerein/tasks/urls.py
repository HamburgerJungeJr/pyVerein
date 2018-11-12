# Import django-urls.
from django.conf.urls import url
# Import views.
from . import views

# Set app name
app_name = 'tasks'
# Set url-patterns
urlpatterns = [
    url(r'^$', views.TaskIndexView.as_view(), name='task_list'),
    url(r'^apply_subscriptions/$', views.apply_subscriptions, name='apply_subscriptions'),
] 
