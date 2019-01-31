# Import django-urls.
from django.conf.urls import url
# Import views.
from . import views

# Set app name
app_name = 'finance'
# Set url-patterns
urlpatterns = [
    url(r'^creditor/$', views.CreditorIndexView.as_view(), name='creditor_list'),
    url(r'^creditor/(?P<pk>[0-9]+)/$', views.CreditorDetailView.as_view(), name='creditor_detail'),
    url(r'^creditor/(?P<pk>[0-9]+)/edit/$', views.CreditorEditView.as_view(), name='creditor_edit'),
    url(r'^creditor/new/$', views.CreditorCreateView.as_view(), name='creditor_create'),
    url(r'^creditor/(?P<account>[0-9]+)/clearing/$', views.CreditorClearingView.as_view(), name='creditor_clear'),

    url(r'^debitor/$', views.DebitorIndexView.as_view(), name='debitor_list'),
    url(r'^debitor/(?P<pk>[0-9]+)/$', views.DebitorDetailView.as_view(), name='debitor_detail'),
    url(r'^debitor/(?P<pk>[0-9]+)/edit/$', views.DebitorEditView.as_view(), name='debitor_edit'),
    url(r'^debitor/new/$', views.DebitorCreateView.as_view(), name='debitor_create'),
    url(r'^debitor/(?P<account>[0-9]+)/clearing/$', views.DebitorClearingView.as_view(), name='debitor_clear'),

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
    url(r'^transaction/(?P<internal_number>[0-9]+)/$', views.TransactionDetailView.as_view(), name='transaction_detail'),
    url(r'^transaction/(?P<internal_number>[0-9]+)/edit/(?P<pk>[0-9]+)/$', views.TransactionEditView.as_view(), name='transaction_edit'),
    url(r'^transaction/new/$', views.TransactionCreateView.as_view(), name='transaction_create'),
    url(r'^transaction/new/(?P<session_id>[a-zA-Z0-9]+)/$', views.TransactionCreateView.as_view(), name='transaction_create_session'),
    url(r'^transaction/new/(?P<session_id>[a-zA-Z0-9]+)/(?P<step>[0-9]+)/$', views.TransactionCreateView.as_view(), name='transaction_create_step'),
    url(r'^transaction/(?P<internal_number>[0-9]+)/reset$', views.reset_transaction, name='transaction_reset'),
    url(r'^transaction/(?P<internal_number>[0-9]+)/reset_new$', views.reset_new_transaction, name='transaction_reset_new'),

    url(r'^api/account/(?P<search>.+)$', views.get_account, name='account_search'),
    url(r'^api/costcenter/(?P<search>.+)$', views.get_cost_center, name='costcenter_search'),
    url(r'^api/costobject/(?P<search>.+)$', views.get_cost_object, name='costobject_search'),
    url(r'^api/clearing/$', views.clear_transaction, name='clear_transactions'),
    url(r'^api/clearing/reset/$', views.reset_cleared_transaction, name='reset_cleared_transactions'),
] 
