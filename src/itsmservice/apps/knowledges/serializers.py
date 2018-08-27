from rest_framework import serializers

from .models import Knowledge


class KnowledgeSerializers(serializers.ModelSerializer):

    class Meta:
        model = Knowledge
        fields = "__all__"
