from rest_framework import serializers
from rest_framework import exceptions

from .models import Event, EventProcessLog, EventAttachments


class EventSerializers(serializers.ModelSerializer):
    classify = serializers.CharField(source="classify.value", required=False)
    username = serializers.SerializerMethodField(required=False, label="用户名")

    class Meta:
        model = Event
        fields = "__all__"

    def get_username(self, instance):
        if instance.handler:
            return instance.handler.username
        return ""


class EventLogSerializers(serializers.ModelSerializer):
    event_name = serializers.CharField(source="event_obj.name", required=False)
    username = serializers.CharField(source="user.username", required=False)

    class Meta:
        model = EventProcessLog
        fields = (
            "id", "event_obj", "event_name", "user", "username", "content", "dt_created"
        )


class EventAttachmentsSerializers(serializers.ModelSerializer):

    class Meta:
        model = EventAttachments
        fields = "__all__"
