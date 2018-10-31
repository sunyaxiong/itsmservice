from rest_framework import serializers
from rest_framework import exceptions

from .models import Change
from .models import ChangeProcessLog


class ChangeSerializers(serializers.ModelSerializer):
    # stage = serializers.CharField(source="get_stage_display")

    class Meta:
        model = Change
        fields = "__all__"

    def validate_stage(self, value):
        if value is not "oook":
            raise exceptions.ValidationError("不合法")
        return value

    def validate_name(self, value):
        if value:
            raise exceptions.ValidationError("名称不可修改")
        return value


class ChangeLogSerializers(serializers.ModelSerializer):
    change_name = serializers.CharField(source="change.name", required=False)
    username = serializers.CharField(source="user.username", required=False)

    class Meta:
        model = ChangeProcessLog
        fields = "__all__"

    def create(self, validated_data):
        # log 提交成功,判断下一节点,失败raise异常,成功跳转.
        print(validated_data)
        change = validated_data["change"]
        next_node_num = change.flow_node + 1
        node_list = change.flow_module.nodes.all()
        print(change.flow_module)
        print(node_list[1])
        return ChangeProcessLog(**validated_data)