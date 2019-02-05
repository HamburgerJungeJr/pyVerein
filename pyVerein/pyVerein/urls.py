"""pyVerein URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include
from django.urls import path
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from django.urls import re_path
from django.views.static import serve

urlpatterns = i18n_patterns(
    path('', include('app.urls')),
    path('account/', include('account.urls'), name='account'),
    path('members/', include('members.urls'), name='members'),
    path('finance/', include('finance.urls'), name='finance'),
    path('reporting/', include('reporting.urls'), name='reporting'),
    path('tasks/', include('tasks.urls'), name='tasks'),
    path('admin/', admin.site.urls),
                            )
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
