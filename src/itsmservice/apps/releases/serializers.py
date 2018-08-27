from rest_framework import serializers

from .models import Release


class ReleaseSerializers(serializers.ModelSerializer):

    class Meta:
        model = Release
        fields = "__all__"
