from django.conf.urls import url
from django.conf.urls import include
from rest_framework import routers

from . import views
from .viewsets import EventViewSet

router = routers.DefaultRouter()
router.register("event", EventViewSet, base_name="EventViewSet")

urlpatterns = [
    url(r'', include(router.urls, namespace='event_rest_api')),
    # 事件管理
    url(r'^event_list/$', views.events),
    url(r'^request_list/$', views.request_list),
    url(r'^incident_list/$', views.incident_list),
    url(r'^events/(?P<pk>\d{1,9})', views.event_detail),
    url(r'^events/add/$', views.event_add),
    url(r'^events/create_order/(?P<pk>\d{1,9})', views.event_create_order),
    url(r'^events/event_to_change/(?P<pk>\d{1,9})', views.event_to_change),
    url(r'^events/event_to_issue/(?P<pk>\d{1,9})', views.event_to_issue),
    url(r'^events/event_upgrade/$', views.event_upgrade),
    url(r'^events/close/(?P<pk>\d{1,9})', views.event_to_close),
]
