from django.db import models

from apps.common.models import BaseModel
from apps.events.models import Event


class SatisfactionLog(BaseModel):
    event = models.ForeignKey(Event, related_name="sati_logs", verbose_name="关联事件")
    comment = models.CharField("满意度", max_length=128, null=True, blank=True)
    content = models.TextField("评价", null=True, blank=True)
    checked = models.BooleanField("状态", default=0)