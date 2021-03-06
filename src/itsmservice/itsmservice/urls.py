"""itsmservice URL Configuration

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
from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.authtoken import views as auth_views

from apps.accounts import views


admin.site.site_header = "伟仕云安ITSM后台管理"
admin.site.site_title = "伟仕云安ITSM后台管理"
admin.site.site_url = None


api_patterns = [
    url(r'', include('apps.urls')),
]

urlpatterns = [
    url(r'^$', views.index),
    url(r'^admin/', admin.site.urls),
    # rest framework jwt 认证接口
    url(r'^login/', obtain_jwt_token),
    # drf自带的token认证模式
    url(r'^api-token-auth/', auth_views.obtain_auth_token),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^configs/', include('apps.configs.urls')),
    url(r'^api/', include('apps.api.urls')),
    url(r'^events/', include('apps.events.urls')),
    url(r'^changes/', include('apps.changes.urls')),
    url(r'^issues/', include('apps.issues.urls')),
    url(r'^accounts/', include('apps.accounts.urls')),
    url(r'^release/', include('apps.releases.urls')),
    url(r'^rest/', include(api_patterns, namespace='rest', app_name='itsm')),
]
