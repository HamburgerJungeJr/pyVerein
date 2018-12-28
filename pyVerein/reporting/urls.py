# Import django-urls.
from django.conf.urls import url
# Import views.
from . import views

# Set app name
app_name = 'reporting'
# Set url-patterns
urlpatterns = [
    url(r'^$', views.ReportIndexView.as_view(), name='list'),
    url(r'^(?P<pk>[0-9]+)/$', views.ReportDetailView.as_view(), name='detail'),
    url(r'^edit/(?P<pk>[0-9]+)/$', views.ReportEditView.as_view(), name='edit'),
    url(r'^new/$', views.ReportCreateView.as_view(), name='create'),
    url(r'^run/(?P<pk>[0-9]+)/$', views.run_report, name='run'),
    url(r'^download_report/(?P<pk>[0-9]+)/$', views.download_report, name='download_report'),
    url(r'^upload_resource/(?P<pk>[0-9]+)/$', views.upload_resource, name='upload_resource'),
    url(r'^delete_resource/(?P<pk>[0-9]+)/$', views.delete_resource, name='delete_resource'),
] 
