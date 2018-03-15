# Import django-urls.
from django.conf.urls import url
# Import views.
from . import views

# Set app name
app_name = 'members'
# Set url-patterns
urlpatterns = [
    url(r'^$', views.MemberIndexView.as_view(), name='list'),
    url(r'^data/$', views.MemberDatatableView.as_view(), name='apiList'),
    url(r'^(?P<pk>[0-9]+)/$', views.MemberDetailView.as_view(), name='detail'),
    url(r'^edit/(?P<pk>[0-9]+)/$', views.MemberEditView.as_view(), name='edit'),
    url(r'^new/$', views.MemberCreateView.as_view(), name='create')
]
