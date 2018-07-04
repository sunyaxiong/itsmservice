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
    # CMDB
    url(r'cmdb/query_vm/$', views.get_vm_list),
    url(r'cmdb/query_disk/$', views.get_disk_list),

    # cloud config
    url(r'cloud/get_product_list/$', views.get_product_list),
    url(r'cloud/get_cluster_list/$', views.get_cluster_list),
    url(r'cloud/get_cluster_role_list/$', views.get_cluster_role_list),
    url(r'cloud/order_create/$', views.order_create),
    url(r'cloud/order_get/$', views.order_get),
    url(r'cloud/user_get/$', views.user_get),
    url(r'cloud/get_instance_list/$', views.get_instance_list),
    url(r'cloud/resource_info/$', views.resource_info),
]
