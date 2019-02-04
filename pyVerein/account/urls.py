# Import django-urls.
from django.urls import path
# Import views.
from . import views
from django.contrib.auth.views import LogoutView
from two_factor.views import DisableView, LoginView, QRGeneratorView, SetupCompleteView, SetupView


# Set app name
app_name = 'account'
# Set url-patterns
urlpatterns = [
    path('', views.UserDetailView.as_view(), name='detail'),
    path('edit/', views.UserEditView.as_view(), name='edit'),
    path('changepassword/', views.change_password, name='change_password'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(), name='login'),
    path('two_factor/setup/', views.SetupView.as_view(), name='two_factor_setup'),
    path('two_factor/qr_code/', QRGeneratorView.as_view(), name='two_factor_qr'),
    path('two_factor/setup/complete/', SetupCompleteView.as_view(), name='two_factor_setup_complete'),
    path('two_factor/backup/tokens/', views.BackupTokensView.as_view(), name='two_factor_backup_tokens'),
    path('two_factor/disable/', DisableView.as_view(), name='two_factor_disable'),
]
