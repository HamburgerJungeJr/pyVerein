# Import django-urls.
from django.urls import path
# Import views.
from . import views

# Set app name
app_name = 'members'
# Set url-patterns
urlpatterns = [
    path('member/', views.MemberIndexView.as_view(), name='member_list'),
    path('member/<int:pk>/', views.MemberDetailView.as_view(), name='member_detail'),
    path('member/edit/<int:pk>/', views.MemberEditView.as_view(), name='member_edit'),
    path('member/new/', views.MemberCreateView.as_view(), name='member_create'),
    path('upload_file/<int:pk>/', views.upload_file, name='member_upload_file'),
    path('delete_file/<int:pk>/', views.delete_file, name='member_delete_file'),
    path('download_file/<int:pk>/', views.download_file, name='member_download_file'),

    path('division/', views.DivisionIndexView.as_view(), name='division_list'),
    path('division/<int:pk>/', views.DivisionDetailView.as_view(), name='division_detail'),
    path('division/edit/<int:pk>/', views.DivisionEditView.as_view(), name='division_edit'),
    path('division/new/', views.DivisionCreateView.as_view(), name='division_create'),

    path('subscription/', views.SubscriptionIndexView.as_view(), name='subscription_list'),
    path('subscription/<int:pk>/', views.SubscriptionDetailView.as_view(), name='subscription_detail'),
    path('subscription/edit/<int:pk>/', views.SubscriptionEditView.as_view(), name='subscription_edit'),
    path('subscription/new/', views.SubscriptionCreateView.as_view(), name='subscription_create')
]
