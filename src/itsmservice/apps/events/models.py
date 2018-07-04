import jsonfield

from django.db import models
from django.contrib.auth.models import User

from lib.models import BaseModel


class Event(BaseModel):

    EVENT_CHOICE = (
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

    TYPE = (
        ("incident", "故障报修"),
        ("request", "服务请求"),
        ("s", "软件配置"),
        ("h", "系统维护"),
        ("n", "网络配置"),
    )

    name = models.CharField(max_length=128, verbose_name="事件名称", null=True, blank=True)
    description = models.TextField(verbose_name="事件描述", null=True, blank=True)
    state = models.CharField(max_length=128, choices=EVENT_CHOICE, verbose_name="事件状态", null=True, blank=True)
    initiator = models.CharField("发起人", max_length=128, null=True, blank=True)
    initiator_phone = models.CharField("发起人电话", max_length=128, null=True, blank=True)
    initiator_email = models.CharField("发起人邮箱", max_length=128, null=True, blank=True)
    initiator_channel = models.CharField("发起人渠道", max_length=128, null=True, blank=True)
    department = models.CharField(max_length=128, verbose_name="部门", null=True, blank=True)
    technician = models.ForeignKey(
        User, verbose_name="处理人", null=True, blank=True
    )
    emergency_degree = models.CharField(
        verbose_name="紧急度", choices=EMERGENCY_DEGREE, max_length=128, null=True, blank=True
    )
    service_level = models.CharField(verbose_name="SLA", max_length=128, null=True, blank=True)
    event_type = models.CharField(
        max_length=128, verbose_name="事件类型", choices=TYPE, null=True, blank=True
    )
    resource = models.CharField(max_length=128, verbose_name="事件源", null=True, blank=True)
    solution = models.TextField(verbose_name="解决方法", null=True, blank=True)
    attach_file = models.FileField(verbose_name="附件", null=True, blank=True)
    flow_module = models.FileField(verbose_name="流程模板", null=True, blank=True)
    cloud_order = models.CharField(verbose_name="云管订单", max_length=128, null=True, blank=True)
    cloud_order_ended = models.BooleanField("订单已完成", default=0)
    app_name = models.CharField("产品名称", max_length=128, null=True, blank=True)
    auto_deploy = models.BooleanField("是否自动化部署订单", default=0)
    leak_checked = models.BooleanField("是否执行漏洞扫描", default=0)
    late_flag = models.BooleanField("是否逾期", default=0)
    instance_id = models.IntegerField("云管实例ID", null=True, blank=True)

    def __str__(self):
        return self.name or ""

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None, *args, **kwargs):
        name = self.app_name
        query_set = ProductInfo.objects.filter(app_name=name).values("app_name")
        app_name_list = [i["app_name"] for i in query_set]
        if name in app_name_list:
            self.auto_deploy = 1
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
    username = models.CharField("用户名", max_length=256, blank=True, null=True)
    content = models.TextField("处理记录", blank=True, null=True)