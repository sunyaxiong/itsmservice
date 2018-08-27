import jsonfield

from django.db import models
from django.contrib.auth.models import User

from apps.accounts.models import Channel
from apps.common.models import BaseModel, BaseFile


class Classify(BaseModel):

    value = models.CharField("类别名称", max_length=128)
    level = models.IntegerField("层级")
    org = models.ForeignKey(Channel, verbose_name="组织")
    parent_level = models.ForeignKey(
        "Classify", verbose_name="父级别菜单", null=True, blank=True
    )


class Event(BaseModel):

    EVENT_STATE_CHOICE = (
        ("draft", "草稿"),
        ("processing", "处理中"),
        ("issued", "转入问题"),
        ("changed", "转入变更"),
        ("checked", "审批完成"),
        ("ended", "结束")
    )

    EMERGENCY_DEGREE = (
        ("P1", "P1"),
        ("P2", "P2"),
        ("P3", "P3")
    )

    PRIORITY = (
        ("0", "低"),
        ("1", "普通"),
        ("2", "中"),
        ("3", "高")
    )

    TYPE = (
        ("incident", "故障报修"),
        ("request", "服务请求"),
        ("s", "软件配置"),
        ("h", "系统维护"),
        ("n", "网络配置"),
    )
    INFLUENCE_SCOPE_CHOICE = (
        ("1", "个人"),
        ("2", "部门"),
        ("3", "组织"),
    )

    name = models.CharField(max_length=128, verbose_name="事件名称", null=True, blank=True)
    description = models.TextField(verbose_name="事件描述", null=True, blank=True)
    state = models.CharField(max_length=128, choices=EVENT_STATE_CHOICE, verbose_name="事件状态", null=True, blank=True)
    initiator = models.ForeignKey(
        User, null=True, blank=True, verbose_name="发起人", related_name="发起人"
    )
    department = models.CharField(max_length=128, verbose_name="部门", null=True, blank=True)
    handler = models.ForeignKey(
        User, verbose_name="处理人", null=True, blank=True
    )
    create_by = models.CharField("创建方式", max_length=128)
    influence_scope = models.CharField(
        "影响范围", choices=INFLUENCE_SCOPE_CHOICE, max_length=128, null=True, blank=True
    )
    located_in = models.CharField("位置", max_length=128, null=True, blank=True)

    emergency_degree = models.CharField(
        verbose_name="紧急度", choices=EMERGENCY_DEGREE, max_length=128, null=True, blank=True
    )
    service_level = models.CharField("SLA", max_length=128, null=True, blank=True)  # TODO 是否关联表
    priority = models.CharField("优先级", max_length=128, choices=PRIORITY)
    classify = models.ForeignKey(Classify, verbose_name="事件分类", null=True, blank=True)

    resource = models.CharField("事件源", max_length=128, null=True, blank=True)  # TODO 事件源

    def __str__(self):
        return self.name or ""

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None, *args, **kwargs):
        # name = self.app_name
        # query_set = ProductInfo.objects.filter(app_name=name).values("app_name")
        # app_name_list = [i["app_name"] for i in query_set]
        # if name in app_name_list:
        #     self.auto_deploy = 1
        super(Event, self).save(*args, **kwargs)


class ProductInfo(BaseModel):

    app_name = models.CharField("应用名称", max_length=128)
    product_id = models.CharField("云管产品ID", max_length=128, default=0)
    cloud_flag = models.CharField("云归属", max_length=128, default=0)
    standard = jsonfield.JSONField("规格", null=True, blank=True)
    vswitch = models.CharField("网络组", max_length=128, null=True, blank=True)

    def __str__(self):
        return self.app_name


class EventProcessLog(BaseModel):

    event_obj = models.ForeignKey(Event, related_name="logs", verbose_name="关联事件")
    username = models.ForeignKey(User, max_length=256, blank=True, null=True)
    content = models.TextField("处理记录", blank=True, null=True)


class EventAttachments(BaseFile):

    event = models.ForeignKey(Event, related_name="event_attachments", verbose_name="附件")
    upload_user = models.ForeignKey(User, verbose_name="上传者")

