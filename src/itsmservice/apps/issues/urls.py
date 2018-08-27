from django.conf.urls import url
from django.conf.urls import include
from rest_framework import routers

from . import views
from .viewsets import IssueViewSet

router = routers.DefaultRouter()
router.register("issue", IssueViewSet, base_name="IssueViewSet")

urlpatterns = [
    url(r'', include(router.urls, namespace='issue_rest_api')),
    # 问题管理
    url(r'^issue_list/$', views.issues),
    url(r'^issues/(?P<pk>\d{1,9})', views.issue_detail),
    url(r'^issues/close/(?P<pk>\d{1,9})', views.issue_close),
    url(r'^issues/upgrade/$', views.issue_upgrade),
    url(r'^issues/issue_to_knowledge/$', views.issue_to_knowledge),
]
