from django.conf.urls import url
from django.conf.urls import include
from rest_framework import routers

from .events.viewsets import EventViewSet
from .issues.viewsets import IssueViewSet
from .changes.viewsets import ChangeViewSet
from .configs.viewsets import ConfigViewSet
from .knowledges.viewsets import KnowledgeViewSet
from .releases.viewsets import ReleaseViewSet

router = routers.DefaultRouter()
router.register("event", EventViewSet, base_name="EventViewSet")
router.register("issue", IssueViewSet, base_name="IssueViewSet")
router.register("change", ChangeViewSet, base_name="ChangeViewSet")
router.register("config", ConfigViewSet, base_name="ConfigViewSet")
router.register("knowledge", KnowledgeViewSet, base_name="KnowledgeViewSet")
router.register("releases", ReleaseViewSet, base_name="ReleaseViewSet")

urlpatterns = [
    url(r'', include(router.urls, namespace='all_rest_api')),
]
