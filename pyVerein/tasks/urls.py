# Import django-urls.
from django.urls import path
# Import views.
from . import views

# Set app name
app_name = 'tasks'
# Set url-patterns
urlpatterns = [
    path('', views.TaskIndexView.as_view(), name='task_list'),
    path('apply_subscriptions/', views.apply_subscriptions, name='apply_subscriptions'),
    path('apply_annualclosure/', views.apply_annualclosure, name='apply_annualclosure'),
    path('delete_terminated_members/', views.delete_terminated_members, name='delete_terminated_members'),
    path('delete_report_data/', views.delete_report_data, name='delete_report_data'),
] 
