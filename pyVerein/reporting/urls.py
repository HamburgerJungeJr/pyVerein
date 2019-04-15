# Import django-urls.
from django.urls import path
# Import views.
from . import views

# Set app name
app_name = 'reporting'
# Set url-patterns
urlpatterns = [
    path('', views.ReportIndexView.as_view(), name='list'),
    path('new/', views.ReportCreateView.as_view(), name='create'),
    path('<int:pk>/', views.ReportDetailView.as_view(), name='detail'),
    path('edit/<int:pk>/', views.ReportEditView.as_view(), name='edit'),
    path('run/<int:pk>/', views.run_report, name='run'),
    path('download_report/<int:pk>/', views.download_report, name='download_report'),
    path('upload_resource/<int:pk>/', views.upload_resource, name='upload_resource'),
    path('delete_resource/<int:pk>/', views.delete_resource, name='delete_resource'),
    path('download_resource/<int:pk>/', views.download_resource, name='download_resource'),
    path('download_data/', views.download_data, name='download_data'),
] 
