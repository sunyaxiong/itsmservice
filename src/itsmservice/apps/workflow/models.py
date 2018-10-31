from django.db import models
from django.contrib.auth.models import User

from apps.common.models import BaseModel
from apps.accounts.models import Channel, JobTitle


class FlowModule(BaseModel):
    name = models.CharField("模板名称", max_length=128)
    org = models.ForeignKey(Channel, verbose_name="归属组织")
    creator = models.ForeignKey(User, verbose_name="创建人")

    def __str__(self):
        return self.name


class FlowNode(BaseModel):
    name = models.CharField("节点名称", max_length=128)
    number = models.IntegerField("节点序号")
    flow_module = models.ForeignKey(
        FlowModule, null=True, blank=True, verbose_name="归属模板", related_name="nodes"
    )
    job_title = models.ForeignKey(
        JobTitle, verbose_name="岗位名称", null=True, blank=True
    )

    def __str__(self):
        return self.name
