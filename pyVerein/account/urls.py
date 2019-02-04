# Import django-urls.
from django.conf.urls import url
# Import views.
from . import views
from django.contrib.auth.views import LogoutView
from two_factor.views import DisableView, LoginView, QRGeneratorView, SetupCompleteView, SetupView


# Set app name
app_name = 'account'
# Set url-patterns
urlpatterns = [
    url(r'^$', views.UserDetailView.as_view(), name='detail'),
    url(r'^edit/$', views.UserEditView.as_view(), name='edit'),
    url(r'^changepassword/$', views.change_password, name='change_password'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^two_factor/setup$', views.SetupView.as_view(), name='two_factor_setup'),
    url(r'^two_factor/qr_code$', QRGeneratorView.as_view(), name='two_factor_qr'),
    url(r'^two_factor/setup/complete$', SetupCompleteView.as_view(), name='two_factor_setup_complete'),
    url(r'^two_factor/backup/tokens$', views.BackupTokensView.as_view(), name='two_factor_backup_tokens'),
    url(r'^two_factor/disable$', DisableView.as_view(), name='two_factor_disable'),
]
