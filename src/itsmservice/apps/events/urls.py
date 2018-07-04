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
    # 事件管理
    url(r'^event_list/$', views.events),
    url(r'^request_list/$', views.request_list),
    url(r'^incident_list/$', views.incident_list),
    url(r'^event/(?P<pk>\d{1,9})', views.event_detail),
    url(r'^events/add/$', views.event_add),
    url(r'^events/create_order/(?P<pk>\d{1,9})', views.event_create_order),
    url(r'^events/event_to_change/(?P<pk>\d{1,9})', views.event_to_change),
    url(r'^events/event_to_issue/(?P<pk>\d{1,9})', views.event_to_issue),
    url(r'^events/event_upgrade/$', views.event_upgrade),
    url(r'^events/close/(?P<pk>\d{1,9})', views.event_to_close),
]
