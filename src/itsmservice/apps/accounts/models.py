import jsonfield

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from lib.models import BaseModel


class Channel(models.Model):
    name = models.CharField(max_length=128, verbose_name="名称", unique=True)

    def __str__(self):
        return self.name


class Department(BaseModel):
    name = models.CharField(max_length=128, verbose_name="名称")
    org = models.ForeignKey("Channel", verbose_name="组织")


class Organization(BaseModel):
    name = models.CharField(max_length=128, verbose_name="名称", unique=True)
    admin = models.ForeignKey(User, verbose_name="管理员")
    event_module = jsonfield.JSONField(verbose_name="事件模板", null=True, blank=True)
    issue_module = jsonfield.JSONField(verbose_name="问题模板", null=True, blank=True)
    change_module = jsonfield.JSONField(verbose_name="变更模板", null=True, blank=True)

    def __str__(self):
        return self.name


class Profile(BaseModel):
    user = models.OneToOneField(User, verbose_name="用户")
    department = models.ForeignKey("Department", verbose_name="部门", null=True, blank=True)
    fit_user_type = models.IntegerField("云管用户类型", default=3)
    phone = models.BigIntegerField("手机号", null=True, blank=True)
    email = models.EmailField("邮箱", null=True, blank=True)
    position = models.CharField("岗位", max_length=128, null=True, blank=True)
    last_reset_pass = models.DateTimeField("上次修改密码时间", null=True, blank=True)

    def __str__(self):
        return self.user.username


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)


# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()



class MessageAlert(BaseModel):
    """
    账户注册审核提醒;
    """
    ACTION_TYPE = (
        ("reg_info", "新用户审核提醒"),
        ("knowledge_info", "知识库审核提醒"),
    )

    user = models.ForeignKey(User)
    initiator = models.CharField("发起人", max_length=128, null=True, blank=True)
    content = models.TextField("提醒内容", null=True, blank=True)
    ins = models.CharField("流程类型", max_length=128, null=True, blank=True)
    ins_id = models.CharField("流程id", max_length=128, null=True, blank=True)
    action_type = models.CharField(
        "动作类型", max_length=128, null=True, blank=True, choices=ACTION_TYPE
    )
    checked = models.BooleanField("是否查看", default=0)

