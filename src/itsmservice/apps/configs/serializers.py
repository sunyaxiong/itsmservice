from rest_framework import serializers

from .models import Config


class ConfigSerializers(serializers.ModelSerializer):

    class Meta:
        model = Config
        fields = "__all__"
