from django.db import models
from apps.common.models import BaseModel


class Knowledge(BaseModel):

    title = models.CharField("名称", max_length=128)
    issue_id = models.IntegerField("问题ID", null=True, blank=True)
    issue_name = models.CharField("问题名称", max_length=128, null=True, blank=True)
    classify = models.CharField("分类", max_length=128, null=True, blank=True)
    state = models.BooleanField("状态", default=0)
    content = models.TextField("内容")
    creater = models.CharField("创建人", max_length=128, null=True, blank=True)
    creater_id = models.IntegerField("创建人ID", null=True, blank=True)
    public_flag = models.IntegerField("是否公开", default=0)
    attach_file = models.FileField("附件", null=True, blank=True)

    def __str__(self):
        return self.title
