from django.db import models
from django.contrib.auth.models import User

from apps.common.models import BaseModel
from apps.events.models import Event, Classify
from apps.common.models import BaseFile


class Issue(BaseModel):

    STATE_CHOICE = (
        ("draft", "草稿"),
        ("processing", "处理中"),
        ("ended", "结束"),
        ("dropped", "废弃"),
    )

    EMERGENCY_DEGREE = (
        ("P1", "P1"),
        ("P2", "P2"),
        ("P3", "P3")
    )

    INFLUENCE_SCOPE_CHOICE = (
        ("1", "个人"),
        ("2", "部门"),
        ("3", "组织"),
    )

    PRIORITY = (
        ("0", "低"),
        ("1", "普通"),
        ("2", "中"),
        ("3", "高")
    )

    name = models.CharField(max_length=128, verbose_name="问题名称")
    description = models.TextField(verbose_name="问题描述")
    classify = models.ForeignKey(Classify, null=True, blank=True, verbose_name="问题分类")
    state = models.CharField(max_length=128, verbose_name="问题状态")
    influence_scope = models.CharField(
        "影响范围", choices=INFLUENCE_SCOPE_CHOICE, max_length=128, null=True, blank=True
    )
    located_in = models.CharField("位置", max_length=128)

    emergency_degree = models.CharField(
        verbose_name="紧急度", choices=EMERGENCY_DEGREE, max_length=128, null=True, blank=True
    )
    service_level = models.CharField("SLA", max_length=128, null=True, blank=True)  # TODO 是否关联表
    priority = models.CharField("优先级", max_length=128, choices=PRIORITY)
    initiator = models.ForeignKey(
        User, null=True, blank=True, verbose_name="发起人", related_name="issue_initiator"
    )
    department = models.CharField(max_length=128, verbose_name="部门", null=True, blank=True)
    handler = models.ForeignKey(
        User, verbose_name="处理人", null=True, blank=True
    )

    event_from = models.ForeignKey(Event, null=True, blank=True, verbose_name="事件源")
    solution = models.TextField(verbose_name="解决方法")
    resource = models.CharField("事件源", max_length=128, null=True, blank=True)  # TODO 事件源

    class Meta:
        app_label = "issues"
        verbose_name = "问题"
        verbose_name_plural = "问题"


class IssueProcessLog(BaseModel):
    issue_obj = models.ForeignKey(Issue, related_name="logs", verbose_name="关联问题")
    username = models.ForeignKey(User, max_length=256, blank=True, null=True, verbose_name="处理人")
    content = models.TextField("处理记录", blank=True, null=True)


class IssueAttachments(BaseFile):

    issue = models.ForeignKey(Event, related_name="attachments", verbose_name="附件")
    upload_user = models.ForeignKey(User, verbose_name="上传者")