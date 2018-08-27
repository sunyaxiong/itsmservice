from rest_framework import serializers

from .models import Change


class ChangeSerializers(serializers.ModelSerializer):

    class Meta:
        model = Change
        fields = "__all__"
