from django.db import models
from django.contrib.auth.models import User

from apps.common.models import BaseModel, BaseFile
from apps.events.models import Event, Classify
from apps.issues.models import Issue
from apps.accounts.models import Department


class Change(BaseModel):
    EMERGENCY_DEGREE = (
        ("P1", "P1"),
        ("P2", "P2"),
        ("P3", "P3"),
    )

    STATE = (
        ("draft", "草稿"),
        ("ing", "流转中"),
        ("ended", "结束"),
        ("failed", "失败"),
    )

    STAGE = (
        ("draft", "提交申请"),
        ("approval", "变更审批"),
        ("Implementation ", "变更实施"),
        ("closed ", "关闭"),
    )

    PRIORITY = (
        ("Low", "低"),
        ("High", "高"),
        ("Medium", "中等"),
        ("Normal ", "正常"),
    )

    INFLUENCE_SCOPE_CHOICE = (
        ("1", "个人"),
        ("2", "部门"),
        ("3", "组织"),
    )

    name = models.CharField(max_length=129, verbose_name="变更名称", null=True, blank=True)
    description = models.TextField(verbose_name="变更描述")
    stage = models.CharField("当前阶段", max_length=128, default="draft", choices=STAGE)
    status = models.CharField("状态", max_length=128, null=True, blank=True)
    classify = models.ForeignKey(Classify, null=True, blank=True, verbose_name="分类")
    emergency_degree = models.CharField(
        verbose_name="紧急度", choices=EMERGENCY_DEGREE, max_length=128, null=True, blank=True
    )
    service_level = models.CharField("SLA", max_length=128, null=True, blank=True)  # TODO 是否关联表
    priority = models.CharField("优先级", max_length=128, choices=PRIORITY)
    influence_scope = models.CharField(
        "影响范围", choices=INFLUENCE_SCOPE_CHOICE, max_length=128, null=True, blank=True
    )
    initiator = models.ForeignKey(User, null=True, blank=True, verbose_name="发起人")
    handler = models.ManyToManyField(
        User, verbose_name="环节处理人", blank=True, related_name="implementer"
    )
    approver = models.ManyToManyField(
        User, verbose_name="环节审批人", blank=True, related_name="approver"
    )
    department = models.ForeignKey(
        Department, max_length=128, verbose_name="部门", null=True, blank=True
    )
    event = models.ManyToManyField(Event, blank=True, verbose_name="关联事件")
    issue = models.ManyToManyField(Issue, blank=True, verbose_name="关联事件")
    node_name = models.CharField(
        max_length=128, verbose_name="流程节点", null=True, blank=True
    )
    located_in = models.CharField("位置", max_length=128)

    start_time = models.DateTimeField("计划开始时间", null=True, blank=True)
    end_times = models.DateTimeField("计划结束时间", null=True, blank=True)
    flow_node = models.IntegerField(verbose_name="当前流程节点", default=0)
    flow_module = models.CharField(verbose_name="流程模板", max_length=128, null=True, blank=True)

    def __str__(self):
        return self.name or ""


class ChangeProcessLog(BaseModel):
    change = models.ForeignKey(Change, related_name="logs", verbose_name="关联变更")
    username = models.ForeignKey(User, blank=True, null=True)
    content = models.TextField("处理记录", blank=True, null=True)
    stage = models.CharField("处理阶段", blank=True, null=True, max_length=128)
    status_before = models.CharField("修改前状态", null=True, blank=True, max_length=128)
    status_after = models.CharField("修改后状态", null=True, blank=True, max_length=128)


class ChangeStage(BaseModel):

    # org = models.ForeignKey(Organization, verbose_name="归属组织")
    name = models.CharField("阶段名称", max_length=128)
    desc = models.TextField("描述")


class StageStatus(BaseModel):
    stage = models.ForeignKey(ChangeStage, verbose_name="关联阶段")
    name = models.CharField("状态名称", max_length=128)
    info_title = models.CharField("通知标题", max_length=128, null=True, blank=True)
    info_content = models.TextField("通知内容", null=True, blank=True)


class ChangeApproveStatus(BaseModel):
    change = models.ForeignKey(Change, verbose_name="关联变更")
    status = models.CharField("审核状态", max_length=128, null=True, blank=True)


class ChangeFile(BaseFile):

    TYPE_CHOICE = (
        ("online", "上线计划"),
        ("rollback", "回退计划"),
        ("review", "回顾文档"),
        ("check_list", "检查表"),
        ("other", "其他")
    )

    change = models.ForeignKey(Change, verbose_name="关联变更")
    creator = models.CharField("创建者", max_length=32, blank=True, null=True)
    type = models.CharField("业务类型", max_length=128, choices=TYPE_CHOICE)


class Role(BaseModel):
    pass