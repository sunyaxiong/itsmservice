import jsonfield

from django.db import models

from apps.common.models import BaseModel


event_module = {"flow": [{"node": 0, "name": "开始"}, {"node": 1, "notify": "邮件", "name": "部门主管"}, {"node": 2, "name": "结束"}], "name": "事件审批"}
change_module = {"flow": [{"node": 0, "name": "开始"}, {"node": 1, "notify": "邮件", "name": "部门主管"}, {"node": 2, "name": "结束"}], "name": "变更审批"}
release_module = {"flow": [{"node": 0, "name": "开始"}, {"node": 1, "notify": "邮件", "name": "部门主管"}, {"node": 2, "name": "结束"}], "name": "发布审批"}
issue_module = {"flow": [{"node": 0, "name": "开始"}, {"node": 1, "notify": "邮件", "name": "部门主管"}, {"node": 2, "name": "结束"}], "name": "问题审批"}
department = {"department": []}


class Config(BaseModel):

    name = models.CharField(max_length=128, verbose_name="名称")
    description = models.TextField(verbose_name="描述", null=True, blank=True)
    state = models.BooleanField(max_length=128, verbose_name="状态", default=1)
    attach_file = models.FileField(verbose_name="附件", null=True, blank=True)
    event_module = jsonfield.JSONField(verbose_name="事件模板", null=True, blank=True, default=event_module)
    issue_module = jsonfield.JSONField(verbose_name="问题模板", null=True, blank=True, default=issue_module)
    change_module = jsonfield.JSONField(verbose_name="变更模板", null=True, blank=True, default=change_module)
    sla_module = jsonfield.JSONField(verbose_name="sla配置", null=True, blank=True)
    department = jsonfield.JSONField("部门维护", null=True, blank=True, default=department)

    def __str__(self):
        return self.name
