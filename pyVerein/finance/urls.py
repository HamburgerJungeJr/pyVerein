# Import django-urls.
from django.urls import path
# Import views.
from . import views

# Set app name
app_name = 'finance'
# Set url-patterns
urlpatterns = [
    path('creditor/', views.CreditorIndexView.as_view(), name='creditor_list'),
    path('creditor/<str:pk>/', views.CreditorDetailView.as_view(), name='creditor_detail'),
    path('creditor/<str:pk>/edit/', views.CreditorEditView.as_view(), name='creditor_edit'),
    path('creditor/new/', views.CreditorCreateView.as_view(), name='creditor_create'),
    path('creditor/<str:account>/clearing/', views.CreditorClearingView.as_view(), name='creditor_clear'),

    path('debitor/', views.DebitorIndexView.as_view(), name='debitor_list'),
    path('debitor/<str:pk>/', views.DebitorDetailView.as_view(), name='debitor_detail'),
    path('debitor/<str:pk>/edit/', views.DebitorEditView.as_view(), name='debitor_edit'),
    path('debitor/new/', views.DebitorCreateView.as_view(), name='debitor_create'),
    path('debitor/<str:account>/clearing/', views.DebitorClearingView.as_view(), name='debitor_clear'),

    path('impersonal/', views.ImpersonalIndexView.as_view(), name='impersonal_list'),
    path('impersonal/<str:pk>/', views.ImpersonalDetailView.as_view(), name='impersonal_detail'),
    path('impersonal/<str:pk>/edit/', views.ImpersonalEditView.as_view(), name='impersonal_edit'),
    path('impersonal/new/', views.ImpersonalCreateView.as_view(), name='impersonal_create'),

    path('costcenter/', views.CostCenterIndexView.as_view(), name='costcenter_list'),
    path('costcenter/<str:pk>/', views.CostCenterDetailView.as_view(), name='costcenter_detail'),
    path('costcenter/<str:pk>/edit/', views.CostCenterEditView.as_view(), name='costcenter_edit'),
    path('costcenter/new/', views.CostCenterCreateView.as_view(), name='costcenter_create'),

    path('costobject/', views.CostObjectIndexView.as_view(), name='costobject_list'),
    path('costobject/<str:pk>/', views.CostObjectDetailView.as_view(), name='costobject_detail'),
    path('costobject/<str:pk>/edit/', views.CostObjectEditView.as_view(), name='costobject_edit'),
    path('costobject/new/', views.CostObjectCreateView.as_view(), name='costobject_create'),

    path('transaction/', views.TransactionIndexView.as_view(), name='transaction_list'),
    path('transaction/<int:internal_number>/', views.TransactionDetailView.as_view(), name='transaction_detail'),
    path('transaction/<int:internal_number>/edit/<int:pk>/', views.TransactionEditView.as_view(), name='transaction_edit'),
    path('transaction/new/', views.TransactionCreateView.as_view(), name='transaction_create'),
    path('transaction/new/<str:session_id>/', views.TransactionCreateView.as_view(), name='transaction_create_session'),
    path('transaction/new/<str:session_id>/<int:step>/', views.TransactionCreateView.as_view(), name='transaction_create_step'),
    path('transaction/<int:internal_number>/reset', views.reset_transaction, name='transaction_reset'),
    path('transaction/<int:internal_number>/reset_new', views.reset_new_transaction, name='transaction_reset_new'),

    path('api/account/<str:search>', views.get_account, name='account_search'),
    path('api/costcenter/<str:search>', views.get_cost_center, name='costcenter_search'),
    path('api/costobject/<str:search>', views.get_cost_object, name='costobject_search'),
    path('api/clearing/', views.clear_transaction, name='clear_transactions'),
    path('api/clearing/reset/', views.reset_cleared_transaction, name='reset_cleared_transactions'),
] 
