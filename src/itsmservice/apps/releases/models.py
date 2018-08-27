from django.db import models
from django.contrib.auth.models import User

from apps.common.models import BaseModel

from apps.changes.models import Change


class Release(BaseModel):
    STAGE = (
        ("draft", "发起"),
        ("ing", "执行中"),
        ("end", "结束"),
        ("failed", "失败"),
    )
    name = models.CharField("发布名称", max_length=128)
    change = models.ForeignKey(Change, verbose_name="关联变更")
    stage = models.CharField("发布阶段", max_length=128, choices=STAGE)
    initiator = models.CharField("发起人", max_length=128, null=True, blank=True)
    technician = models.ForeignKey(User, max_length=128, verbose_name="处理人", null=True, blank=True)
