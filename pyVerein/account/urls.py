# Import django-urls.
from django.conf.urls import url
# Import views.
from . import views
from django.contrib.auth.views import LogoutView

# Set app name
app_name = 'account'
# Set url-patterns
urlpatterns = [
    url(r'^$', views.UserDetailView.as_view(), name='detail'),
    url(r'^edit/$', views.UserEditView.as_view(), name='edit'),
    url(r'^changepassword/$', views.change_password, name='change_password'),
    url(r'^logout/$', LogoutView.as_view(), name='logout')
]
