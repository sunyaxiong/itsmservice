import logging

from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect

from itsmservice import settings
from apps.accounts.models import Channel, Profile
from .models import Change, ChangeProcessLog
from .forms import ChangeDetailForm, ChangeDetailModelForm

logger = logging.getLogger("django")


def changes(request):
    cmp_url = settings.CMP_URL
    page_header = "变更管理"
    data = Change.objects.filter().order_by("-dt_created")
    count = data.count()

    return render(request, 'change_list.html', locals())


def change_detail(request, pk):
    page_header = "变更管理"
    change = Change.objects.get(id=int(pk))
    solution_list = change.logs.all().order_by("-dt_created") if change.logs else []
    user_list = User.objects.all()
    degree_choice_list = Change.EMERGENCY_DEGREE
    host = settings.INTERNET_HOST

    initiator_obj = Profile.objects.filter(username=change.initiator).first()

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

        return render(request, 'change_detail.html', locals())
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

            if data.get("solution"):
                ChangeProcessLog.objects.create(
                    change_obj=change,
                    username=data.get("node_handler"),
                    content=data.get("solution"),
                )

            change.save()
            return HttpResponseRedirect("/itsm/change_list/")
        else:
            print(change_form)
            messages.warning(request, change_form.errors)
        return render(request, 'change_detail.html', locals())


def flow_pass(request):
    """
    传入流程实例,根据流程实例状态判断下一步动作
    :param request:
    :return:
    """

    url = request.META.get('HTTP_REFERER')

    if request.method == "POST":
        form = ChangeDetailForm(request.POST)
        if form.is_valid():
            data = form.data
            try:
                change_id = data.get("id")
                # 当前流程节点信息
                change = Change.objects.get(id=change_id)
                now_node = int(change.flow_node)

                # 获取模板信息
                try:
                    channel = Channel.objects.get(name="伟仕云安")
                    module = channel.change_module
                except Exception as e:
                    messages.warning(request, "模板获取失败")
                    return HttpResponseRedirect(url)

                next_node = now_node + 1
                next_node_name = module["flow"][next_node]["name"] if module else ""

                if next_node_name == "结束":
                    change.state = "ended"

                # TODO 环节处理人,根据模板查询
                node_username = change.node_handler.username
                profile = Profile.objects.get(username=node_username)
                channel_name = profile.channel_name
                try:
                    next_node_handler_profile = Profile.objects.get(channel_name=channel_name, position=next_node_name)
                    next_node_handler_name = next_node_handler_profile.username
                except Exception as e:
                    messages.warning(request, "{}, {}-{}岗位信息未维护".format(e, channel_name, next_node_name))
                    next_node_handler_name = "syx"
                    return HttpResponseRedirect(url)

                next_node_handler = User.objects.get(username=next_node_handler_name)

                # 修改
                if change.state == "draft":
                    change.state = "ing"
                if next_node == len(module["flow"]):
                    change.state = "ended"

                # 更新操作记录 节点加1
                if data.get("solution"):
                    ChangeProcessLog.objects.create(
                        change_obj=change,
                        username=request.user.username,
                        content=data.get("solution")
                    )
                change.node_handler = next_node_handler
                change.flow_node = next_node
                change.node_name = next_node_name
                # node_handler = User.objects.get(username=next_node_handler_profile.username)
                # change.node_handler = node_handler

                change.save()
            except Exception as e:
                messages.info(request, "debug: {}".format(e))
                return HttpResponseRedirect(url)
            messages.info(request, "跳转成功")
            return HttpResponseRedirect(url)
        messages.warning(request, form.errors)
        return HttpResponseRedirect(url)


def change_add(request):
    page_header = "变更管理"

    if request.method == "GET":
        form = ChangeDetailModelForm()
        return render(request, 'new_change_detail.html', locals())
    elif request.method == "POST":
        form = ChangeDetailModelForm(request.POST)

        form.save()
        return HttpResponseRedirect("/itsm/change_list")


def change_close(request, pk):
    url = request.META.get('HTTP_REFERER')
    try:
        change = Change.objects.get(id=pk)
        if change.state == "ended":
            messages.warning(request, "当前变更已关闭")
            return HttpResponseRedirect(url)
        if change.node_handler_id is not request.user.id:
            messages.warning(request, "您不是当前处理人,无法处理该变更")
            return HttpResponseRedirect(url)

        # 执行关闭
        change.state = "ended"
        change.save()
        return HttpResponseRedirect(url)
    except Exception as e:
        messages.warning(request, "变更查询异常: {}".format(e))
        return HttpResponseRedirect(url)


def change_to_config(request):
    pass


def change_reject_back(request):

    url = request.META.get('HTTP_REFERER')

    change_id = request.GET.get("id")

    # 获取变更对象,并修改状态
    change = Change.objects.filter(id=change_id).first()
    if change.state == "draft":
        messages.warning(request, "事件未提交")
        return HttpResponseRedirect(url)
    change.state = "draft"
    change.flow_node = 0
    change.node_name = "开始"
    change.save()

    return HttpResponseRedirect(url)
