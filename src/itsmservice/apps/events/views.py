import time
import logging
import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, HttpResponseRedirect

from lib.fit2cloud import Fit2CloudClient
from itsmservice import settings
from .models import Event, EventProcessLog, ProductInfo
from .forms import EventDetailForm, EventDetailModelForm
from apps.accounts.models import MessageAlert, Profile
from apps.changes.models import Change
from apps.issues.models import Issue
from apps.slas.models import SatisfactionLog

logger = logging.getLogger("django")


@login_required
def events(request):
    cmp_url = settings.CMP_URL
    page_header = "事件管理"

    # 系统管理员全部权限
    if request.user.is_superuser:
        data = Event.objects.filter().order_by("-dt_created")
    else:
        data = Event.objects.filter(
            Q(technician=request.user) | Q(initiator=request.user.username)
        ).order_by("-dt_created")
    count = data.count()

    message_alert_queryset = MessageAlert.objects.filter(
        user=request.user,
        checked=0,
    )
    message_alert_count = message_alert_queryset.count()

    return render(request, 'event_list.html', locals())


@login_required
def request_list(request):
    cmp_url = settings.CMP_URL
    page_header = "事件管理"

    # 系统管理员全部权限
    if request.user.is_superuser:
        data = Event.objects.filter(event_type="request").order_by("-dt_created")
    else:
        data = Event.objects.filter(
            event_type="request",
        ).filter(
            Q(technician=request.user) | Q(initiator=request.user.username)
        ).order_by("-dt_created")

    count = data.count()

    return render(request, 'event_list.html', locals())


@login_required
def incident_list(request):

    cmp_url = settings.CMP_URL
    page_header = "事件管理"
    # data = Event.objects.filter(event_type="incident").order_by("-dt_created")

    # 系统管理员全部权限
    if request.user.is_superuser:
        data = Event.objects.filter(event_type="incident").order_by("-dt_created")
    else:
        data = Event.objects.filter(
            event_type="incident",
        ).filter(
            Q(technician=request.user) | Q(initiator=request.user.username)
        ).order_by("-dt_created")
    count = data.count()

    return render(request, 'event_list.html', locals())


def event_detail(request, pk):
    page_header = "事件管理"
    event = Event.objects.get(id=int(pk))
    solution_list = event.logs.all() if event.logs else []
    user_list = User.objects.all()
    degree_choice_list = Event.EMERGENCY_DEGREE
    button_submit = "保存"
    host = settings.INTERNET_HOST

    # 用户\管理员监控url不同
    profile = Profile.objects.filter(username=request.user.username).first()

    # 根据事件状态控制前端显示
    button_submit = "提交" if event.state == "draft" else "保存"
    display = 0 if event.state == "ended" else 1
    checked = 1 if event.state == "checked" else 0

    if request.method == "GET":

        return render(request, 'event_detail1.html', locals())
    elif request.method == "POST":

        # form收敛数据
        event_form = EventDetailForm(request.POST)
        if event_form.is_valid():
            data = event_form.data

            if data.get("leak_checked") == "是":
                event.leak_checked = 1

            if data.get("emergency_degree"):
                event.emergency_degree = data["emergency_degree"]

            if not data.get("technician") == "None":
                tc = User.objects.filter(username=data.get("technician"))
                event.technician = tc[0]

            if data.get("attach_file"):
                event.attach_file = data.get("attach_file")

            if event.state == "draft":
                button_submit = "提交"
                event.state = "processing"

            # 更新解决方案
            if data.get("solution"):
                EventProcessLog.objects.create(
                    event_obj=event,
                    username=data.get("technician"),
                    content=data.get("solution"),
                )
            event.save()
            return HttpResponseRedirect("/events/event_list/")
        messages.warning(request, event_form.errors)
        return render(request, 'event_detail1.html', locals())


def event_add(request):
    page_header = "事件管理"
    url = request.META.get('HTTP_REFERER')
    if request.method == "GET":
        form = EventDetailModelForm()
        return render(request, 'itsm/new_event_detail.html', locals())
    elif request.method == "POST":
        form = EventDetailModelForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            messages.warning(request, "异常: {}".format(form.errors))
            return HttpResponseRedirect(url)
        return HttpResponseRedirect("/events/event_list/")


def event_create_order(request, pk):
    url = request.META.get('HTTP_REFERER')
    try:
        event = Event.objects.get(id=pk)
        if event.state == "draft":
            messages.warning(request, "当前事件未提交")
            return HttpResponseRedirect(url)
        if event.technician_id is not request.user.id:
            messages.warning(request, "您不是当前处理人,无法关闭事件")
            return HttpResponseRedirect(url)

        if event.event_type == "request":

            # 应用对照信息查询
            app_name = event.app_name
            product_info = ProductInfo.objects.filter(app_name=app_name)
            if not product_info:
                messages.warning(request, "当前应用名称无法部署,请联系管理员维护应用对照信息")
                return HttpResponseRedirect(url)

            # 云管订单创建
            param = {
                "time_stamp": int(round(time.time() * 1000)),
            }
            post = {
                "clusterRoleId": 1,
                "count": 1,
                "description": "需要机器配置：1c1g",
                "expireTime": 4679277169,
                "installAgent": True,
                "productId": product_info[0].product_id
            }
            # 用户信息查询
            _conf = settings.CLOUD_CONF.copy()
            user_res = Fit2CloudClient(_conf, settings.cloud_secret_key).user_get(
                {"time_stamp": int(round(time.time() * 1000))}
            )
            if user_res.get("success"):
                user_data = user_res.get("data")
                user_info = {i["name"]: i for i in user_data}
                user_email = user_info[request.user.username]["email"]
                _conf["user"] = user_email
                # 工作空间接口请求
                ak, sk = Fit2CloudClient(
                    _conf, settings.cloud_secret_key
                ).get_work_space(param)

                if ak and sk:
                    _param = {
                        "time_stamp": int(round(time.time() * 1000)),
                    }
                    # _conf = settings.CLOUD_CONF.copy()
                    _conf["access_key"] = ak
                    order = Fit2CloudClient(_conf, sk).order_create(_param, json.dumps(post))
                    logger.info("新生成订单:  ", order)
                    event.cloud_order = order.get("data")
        else:
            # TODO 故障报修事件关闭逻辑
            pass
        # 执行关闭
        event.state = "ended"
        event.save()
        return HttpResponseRedirect(url)
    except Exception as e:
        messages.warning(request, "事件查询异常: {}".format(e))
        return HttpResponseRedirect(url)


def event_to_change(request, pk):

    url = request.META.get('HTTP_REFERER')

    try:
        event = Event.objects.get(id=pk)
        Change.objects.create(
            name=event.name,
            state="draft",
            node_handler=event.technician,
            initiator=event.technician.username,
            emergency_degree="P3",
            event=event,
        )
        return HttpResponseRedirect("/changes/change_list")
    except Exception as e:
        messages.warning(request, "事件id{}未找到: {}".format(pk, e))
        return HttpResponseRedirect(url)


def event_to_issue(request, pk):

    url = request.META.get('HTTP_REFERER')

    try:
        event = Event.objects.get(id=pk)
        Issue.objects.create(
            name=event.name,
            state="on",
            handler=event.technician,
            event_from=event,
        )
        return HttpResponseRedirect("/issues/issue_list")
    except Exception as e:
        messages.warning(request, "事件id{}未找到: {}".format(pk, e))
        return HttpResponseRedirect(url)


def event_upgrade(request):

    url = request.META.get('HTTP_REFERER')
    username = request.GET.get("username")
    event_id = request.GET.get("event_id")
    logging.warning("ajax test: {}: {}: {}".format(url, username, event_id))

    technician = User.objects.filter(username=username)
    event = Event.objects.filter(id=event_id)[0]
    event.technician = technician[0]
    event.save()

    return HttpResponseRedirect(url)


def event_to_close(request, pk):
    url = request.META.get("HTTP_REFERER")

    event = Event.objects.filter(id=pk)
    if event:
        # 检查漏扫
        if not event.first().leak_checked:
            messages.warning(request, "请执行漏洞扫描")
            return HttpResponseRedirect(url)

        # 根据事件创建满意度调查
        sati_log = SatisfactionLog.objects.create(
            event=event[0]
        )
        # 组织邮件
        mail_to = event[0].initiator_email
        link = "http://itsm.ecscloud.com/slas/satisfaction/?log_id={}".format(sati_log.id)
        message = "您好,您的事件:{}已经处理完成,请对我们的服务做出评价,感谢您的支持. {}".format(
            event[0].name, link
        )
        send_mail("满意度调查", message, settings.EMAIL_HOST_USER, [mail_to])
        logger.info("满意度调查发送成功")

        # 修改事件状态
        event[0].state = "ended"
        event[0].save()
        return HttpResponseRedirect(url)
    else:
        messages.warning(request, "事件不存在,无法关闭,请联系管理员")
        return HttpResponseRedirect(url)
