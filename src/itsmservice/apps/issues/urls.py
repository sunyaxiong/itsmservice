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
from django.contrib import admin

from . import views


urlpatterns = [
    # 问题管理
    url(r'^issue_list/$', views.issues),
    url(r'^issue/(?P<pk>\d{1,9})', views.issue_detail),
    url(r'^issue/close/(?P<pk>\d{1,9})', views.issue_close),
    url(r'^issue/upgrade/$', views.issue_upgrade),
    url(r'^issue/issue_to_knowledge/$', views.issue_to_knowledge),
]
