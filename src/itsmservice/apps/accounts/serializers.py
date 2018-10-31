from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError


from .models import Profile
from .models import Channel
from .models import JobTitle
from .models import Department


class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = "__all__"


class JobTitleSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer()

    class Meta:
        model = JobTitle
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):
    job_title = JobTitleSerializer()
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = "__all__"

    def get_avatar_url(self, instance):
        if instance.avatar:
            return instance.avatar.url
    # def validate_username(self, value):
    #     try:
    #         user = User.objects.get(username=value)
    #     except Exception as e:
    #         raise ValidationError(e)


class ChannelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Channel
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = "__all__"
