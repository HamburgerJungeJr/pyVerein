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
    url(r'^apply_annualclosure/$', views.apply_annualclosure, name='apply_annualclosure'),
    url(r'^delete_terminated_members/$', views.delete_terminated_members, name='delete_terminated_members'),
    url(r'^delete_report_data/$', views.delete_report_data, name='delete_report_data'),
] 
