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

    url(r'^costcenter/$', views.CostCenterIndexView.as_view(), name='costcenter_list'),
    url(r'^costcenter/data/$', views.CostCenterDatatableView.as_view(), name='costcenter_apiList'),
    url(r'^costcenter/(?P<pk>[0-9]+)/$', views.CostCenterDetailView.as_view(), name='costcenter_detail'),
    url(r'^costcenter/(?P<pk>[0-9]+)/edit/$', views.CostCenterEditView.as_view(), name='costcenter_edit'),
    url(r'^costcenter/new/$', views.CostCenterCreateView.as_view(), name='costcenter_create'),

    url(r'^costobject/$', views.CostObjectIndexView.as_view(), name='costobject_list'),
    url(r'^costobject/data/$', views.CostObjectDatatableView.as_view(), name='costobject_apiList'),
    url(r'^costobject/(?P<pk>[0-9]+)/$', views.CostObjectDetailView.as_view(), name='costobject_detail'),
    url(r'^costobject/(?P<pk>[0-9]+)/edit/$', views.CostObjectEditView.as_view(), name='costobject_edit'),
    url(r'^costobject/new/$', views.CostObjectCreateView.as_view(), name='costobject_create'),

    url(r'^transaction/$', views.TransactionIndexView.as_view(), name='transaction_list'),
    url(r'^transaction/data/$', views.TransactionDatatableView.as_view(), name='transaction_apiList'),
    url(r'^transaction/(?P<pk>[0-9]+)/$', views.TransactionDetailView.as_view(), name='transaction_detail'),
    url(r'^transaction/(?P<pk>[0-9]+)/edit/$', views.TransactionEditView.as_view(), name='transaction_edit'),
    url(r'^transaction/new/$', views.TransactionCreateView.as_view(), name='transaction_create'),
    url(r'^transaction/new/(?P<document_number>.+)/$', views.TransactionCreateContinueView.as_view(), name='transaction_create_continue'),

    url(r'^api/account/(?P<search>.+)$', views.get_account, name='account_search'),
    url(r'^api/costcenter/(?P<search>.+)$', views.get_cost_center, name='costcenter_search'),
    url(r'^api/costobject/(?P<search>.+)$', views.get_cost_object, name='costobject_search'),
] 
