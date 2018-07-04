from django.db import models
from django.contrib.auth.models import User

from lib.models import BaseModel
from apps.events.models import Event


class Change(BaseModel):
    EMERGENCY_DEGREE = (
        ("P1", "P1"),
        ("P2", "P2"),
        ("P3", "P3"),
    )

    STATE = (
        ("draft", "草稿"),
        ("ing", "流转中"),
        ("ended", "结束"),
        ("failed", "失败"),
    )

    name = models.CharField(max_length=129, verbose_name="变更名称", null=True, blank=True)
    description = models.TextField(verbose_name="变更描述")
    state = models.CharField(max_length=128, choices=STATE, default="draft", verbose_name="变更状态")
    initiator = models.CharField(max_length=128, null=True, blank=True, verbose_name="发起人")
    department = models.CharField(max_length=128, verbose_name="部门", null=True, blank=True)
    event = models.ForeignKey(Event, null=True, blank=True, verbose_name="关联事件")
    node_name = models.CharField(max_length=128, verbose_name="流程节点", null=True, blank=True)
    node_handler = models.ForeignKey(User, verbose_name="环节处理人", null=True, blank=True)
    emergency_degree = models.CharField(
        verbose_name="紧急度", max_length=128, null=True, blank=True,
    )
    service_level = models.CharField(verbose_name="SLA", max_length=128, null=True, blank=True)
    approver = models.CharField(verbose_name="变更评审", max_length=128, null=True, blank=True)
    # event_from = models.ForeignKey(VMInstance, null=True, blank=True, verbose_name="事件源")
    solution = models.TextField(verbose_name="解决方法", null=True, blank=True)
    online_plan = models.FileField(verbose_name="上线计划", null=True, blank=True)
    rollback_plan = models.FileField(verbose_name="回滚计划", null=True, blank=True)
    flow_node = models.IntegerField(verbose_name="当前流程节点", default=0)
    flow_module = models.CharField(verbose_name="流程模板", max_length=128, null=True, blank=True)
    leak_checked = models.BooleanField("漏洞扫描", default=0)

    def __str__(self):
        return self.name or ""


class ChangeProcessLog(BaseModel):
    change_obj = models.ForeignKey(Change, related_name="logs", verbose_name="关联变更")
    username = models.CharField("用户名", max_length=256, blank=True, null=True)
    content = models.TextField("处理记录", blank=True, null=True)
