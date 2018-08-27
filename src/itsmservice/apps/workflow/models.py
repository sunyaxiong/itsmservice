from django.db import models
from django.contrib.auth.models import User

from apps.common.models import BaseModel
from apps.accounts.models import Channel, JobTitle


class FlowNode(BaseModel):
    name = models.CharField("节点名称", max_length=128)
    number = models.IntegerField("节点序号")
    job_title = models.ForeignKey(JobTitle, verbose_name="岗位名称")


class FlowModule(BaseModel):
    name = models.CharField("模板名称", max_length=128)
    org = models.ForeignKey(Channel, verbose_name="归属组织")
    creator = models.ForeignKey(User, verbose_name="创建人")
