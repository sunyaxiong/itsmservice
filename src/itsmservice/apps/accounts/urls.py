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

from apps.accounts.django_cas_ng import views
from .views import (
    user_profile, pwd_restet, login
)

urlpatterns = [
    # url(r'^login/$', login),
    # url(r'^logout/$', logout),
    url(r'^register/$', views.register, name='cas_ng_register'),
    url(r'^active/(?P<active_code>\d{1,9})', views.active, name='cas_ng_active'),
    url(r'^login/$', views.login, name='cas_ng_login'),
    url(r'^logout/$', views.logout, name='cas_ng_logout'),
    url(r'^callback/$', views.callback, name='cas_ng_proxy_callback'),
    url(r'^user_profile/$', user_profile, name='user profile'),
    url(r'^pwd_reset/$', pwd_restet, name='pwd reset'),

    url(r'^login1/$', login, name='mylogin'),

]