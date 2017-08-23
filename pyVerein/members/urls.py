# Import django-urls.
from django.conf.urls import url
# Import views.
from . import views

# Set app name
app_name = 'members'
# Set url-patterns
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^api/list$', views.DatatableAPI.as_view(), name='apiList'),
    url(r'^(?P<pk>[0-9]+)/$', views.MemberDetailView.as_view(), name='detail')
]
