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
from rest_framework import routers

from . import views
from .viewsets import ChangeViewSet

router = routers.DefaultRouter()
router.register("change", ChangeViewSet, base_name="ChangeViewSet")

urlpatterns = [
    url(r'', include(router.urls, namespace='change_rest_api')),
    # 变更管理
    url(r'^change_list/$', views.changes),
    url(r'^change/(?P<pk>\d{1,9})', views.change_detail),
    url(r'^change/pass/$', views.flow_pass),
    url(r'^change/reject/$', views.change_reject_back),
    url(r'^changes/add/$', views.change_add),
    url(r'^changes/change_to_config/(?P<pk>\d{1,9})', views.change_to_config),
    url(r'^changes/close/(?P<pk>\d{1,9})', views.change_close),
]

