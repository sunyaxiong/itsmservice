import json
import logging

from django.shortcuts import render, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from itsmservice import settings
from apps.accounts.models import Profile, MessageAlert
from apps.changes.models import Change
from apps.changes.forms import ChangeDetailForm
from .models import Release

logger = logging.getLogger(__name__)


@login_required
def releases(request):

    page_header = "发布管理"

    # 系统管理员全部权限
    if request.user.is_superuser:
        data = Change.objects.filter().order_by("dt_created")
    else:
        data = Change.objects.filter().order_by("dt_created")
    count = data.count()

    message_alert_queryset = MessageAlert.objects.filter(
        user=request.user,
        checked=0,
    )
    message_alert_count = message_alert_queryset.count()

    count = data.count()

    return render(request, 'release_list.html', locals())


def release_detail(request, pk):
    page_header = "发布管理"
    change = Change.objects.get(id=int(pk))
    solution_list = change.logs.all().order_by("-dt_created") if change.logs else []
    user_list = User.objects.all()
    degree_choice_list = Change.EMERGENCY_DEGREE
    host = settings.INTERNET_HOST

    # 用户\管理员监控url不同
    profile = Profile.objects.filter(username=request.user.username).first()

    # 根据事件状态控制按钮显隐和名称
    button_submit = "提交" if change.state == "draft" else "同意"
    display = 0 if change.state == "ended" else 1

    if button_submit == "提交":
        action = "/itsm/change/{}".format(change.id)
    elif button_submit == "同意":
        action = "/itsm/change/pass/"

    change_form = ChangeDetailForm()
    if request.method == "GET":

        return render(request, 'release_detail.html', locals())
    elif request.method == "POST":

        # form收敛数据
        change_form = ChangeDetailForm(request.POST)
        if change_form.is_valid():
            logger.info("变更数据收敛成功")
            data = change_form.data
            if change.state == "draft":
                change.state = "ing"
            if data.get("emergency_degree"):
                change.emergency_degree = data.get("emergency_degree")

            change.save()
            return HttpResponseRedirect("/itsm/release_list/")
        else:
            print(change_form)
            messages.warning(request, change_form.errors)
        return render(request, 'change_detail.html', locals())
