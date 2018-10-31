from django.conf.urls import url
from django.conf.urls import include
from rest_framework import routers
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer

from .events.viewsets import EventViewSet, EventLogViewSet
from .events.viewsets import EventAttachmentsViewSet
from .issues.viewsets import IssueViewSet
from .changes.viewsets import ChangeViewSet
from .changes.viewsets import ChangLogViewSet
from .configs.viewsets import ConfigViewSet
from .knowledges.viewsets import KnowledgeViewSet
from .releases.viewsets import ReleaseViewSet
from .accounts.viewsets import UserViewSet
from .accounts.viewsets import ProfileViewSet

router = routers.DefaultRouter()
router.register("event", EventViewSet, base_name="EventViewSet")
router.register("event_log", EventLogViewSet, base_name="EventLogViewSet")
router.register("event_att", EventAttachmentsViewSet, base_name="EventAttachmentsViewSet")
router.register("issue", IssueViewSet, base_name="IssueViewSet")
router.register("change", ChangeViewSet, base_name="ChangeViewSet")
router.register("change_log", ChangLogViewSet, base_name="ChangLogViewSet")
router.register("config", ConfigViewSet, base_name="ConfigViewSet")
router.register("knowledge", KnowledgeViewSet, base_name="KnowledgeViewSet")
router.register("releases", ReleaseViewSet, base_name="ReleaseViewSet")
router.register("user", UserViewSet, base_name="UserViewSet")
router.register("profile", ProfileViewSet, base_name="ProfileViewSet")

schema_view = get_schema_view(title="ITSM 文档", renderer_classes=(SwaggerUIRenderer, OpenAPIRenderer))

urlpatterns = [
    url(r'', include(router.urls, namespace='all_rest_api')),
    url(r'docs/', schema_view, name='ITSM'),
]
