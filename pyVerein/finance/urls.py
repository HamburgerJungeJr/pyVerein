# Import django-urls.
from django.conf.urls import url
# Import views.
from . import views

# Set app name
app_name = 'finance'
# Set url-patterns
urlpatterns = [
    url(r'^creditor/$', views.CreditorIndexView.as_view(), name='creditor_list'),
    url(r'^creditor/data/$', views.CreditorDatatableView.as_view(), name='creditor_apiList'),
    url(r'^creditor/(?P<pk>[0-9]+)/$', views.CreditorDetailView.as_view(), name='creditor_detail'),
    url(r'^creditor/(?P<pk>[0-9]+)/edit/$', views.CreditorEditView.as_view(), name='creditor_edit'),
    url(r'^creditor/new/$', views.CreditorCreateView.as_view(), name='creditor_create'),

    url(r'^debitor/$', views.DebitorIndexView.as_view(), name='debitor_list'),
    url(r'^debitor/data/$', views.DebitorDatatableView.as_view(), name='debitor_apiList'),
    url(r'^debitor/(?P<pk>[0-9]+)/$', views.DebitorDetailView.as_view(), name='debitor_detail'),
    url(r'^debitor/(?P<pk>[0-9]+)/edit/$', views.DebitorEditView.as_view(), name='debitor_edit'),
    url(r'^debitor/new/$', views.DebitorCreateView.as_view(), name='debitor_create'),

    url(r'^impersonal/$', views.ImpersonalIndexView.as_view(), name='impersonal_list'),
    url(r'^impersonal/data/$', views.ImpersonalDatatableView.as_view(), name='impersonal_apiList'),
    url(r'^impersonal/(?P<pk>[0-9]+)/$', views.ImpersonalDetailView.as_view(), name='impersonal_detail'),
    url(r'^impersonal/(?P<pk>[0-9]+)/edit/$', views.ImpersonalEditView.as_view(), name='impersonal_edit'),
    url(r'^impersonal/new/$', views.ImpersonalCreateView.as_view(), name='impersonal_create'),
] 
