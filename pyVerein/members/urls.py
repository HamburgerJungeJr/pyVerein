# Import django-urls.
from django.conf.urls import url
# Import views.
from . import views

# Set app name
app_name = 'members'
# Set url-patterns
urlpatterns = [
    url(r'^member/$', views.MemberIndexView.as_view(), name='list'),
    url(r'^member/data/$', views.MemberDatatableView.as_view(), name='apiList'),
    url(r'^member/(?P<pk>[0-9]+)/$', views.MemberDetailView.as_view(), name='detail'),
    url(r'^member/edit/(?P<pk>[0-9]+)/$', views.MemberEditView.as_view(), name='edit'),
    url(r'^member/new/$', views.MemberCreateView.as_view(), name='create'),

    url(r'^division/$', views.DivisionIndexView.as_view(), name='division_list'),
    url(r'^division/data/$', views.DivisionDatatableView.as_view(), name='division_apiList'),
    url(r'^division/(?P<pk>[0-9]+)/$', views.DivisionDetailView.as_view(), name='division_detail'),
    url(r'^division/edit/(?P<pk>[0-9]+)/$', views.DivisionEditView.as_view(), name='division_edit'),
    url(r'^division/new/$', views.DivisionCreateView.as_view(), name='division_create')
]
