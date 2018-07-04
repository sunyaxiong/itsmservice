from django.db import models
from django.contrib.auth.models import User

from lib.models import BaseModel
from apps.events.models import Event


class Issue(BaseModel):

    name = models.CharField(max_length=128, verbose_name="问题名称")
    description = models.TextField(verbose_name="问题描述")
    state = models.CharField(max_length=128, verbose_name="问题状态")
    issue_type = models.CharField(max_length=128, null=True, blank=True, verbose_name="类型")
    handler = models.ForeignKey(User, verbose_name="处理人", null=True, blank=True)
    event_from = models.ForeignKey(Event, null=True, blank=True, verbose_name="事件源")
    solution = models.TextField(verbose_name="解决方法")
    attach_file = models.FileField(verbose_name="附件", null=True, blank=True)

    class Meta:
        app_label = "issues"
        verbose_name = "问题"
        verbose_name_plural = "问题"


class IssueProcessLog(BaseModel):
    issue_obj = models.ForeignKey(Issue, related_name="logs", verbose_name="关联问题")
    username = models.CharField("用户名", max_length=256, blank=True, null=True)
    content = models.TextField("处理记录", blank=True, null=True)
