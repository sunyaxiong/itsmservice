import logging

from django.shortcuts import render, HttpResponse


from .forms import SatisfactionForm
from apps.events.models import Event
from apps.changes.models import Change
from apps.issues.models import Issue
from apps.accounts.models import MessageAlert
from .models import SatisfactionLog

logger = logging.getLogger(__name__)


def sla_dashboard(request):

    page_header = "SLA水平管理"

    event_count = Event.objects.all().count()
    change_count = Change.objects.all().count()
    issue_count = Issue.objects.all().count()
    releases_count = Change.objects.all().count()

    message_alert_queryset = MessageAlert.objects.filter(
        user=request.user,
        checked=0,
    )
    message_alert_count = message_alert_queryset.count()

    if request.method == "POST":
        pass
    else:
        return render(request, "sla_dashboard.html", locals())


def sla_event_dash(request):

    page_header = "SLA水平管理-事件分析"

    event_queryset = Event.objects.all()
    event_sum_count = event_queryset.count()
    # 事件量统计
    req_count = event_queryset.filter(event_type="request").count()
    incident_count = event_queryset.filter(event_type="incident").count()
    done_event_count = event_queryset.filter(state="ended").count()
    ing_event_count = event_queryset.exclude(state="ended").count()

    late_event = event_queryset.filter(late_flag=1).count()
    normal_event = event_queryset.exclude(late_flag=1).count()
    done_p1_event = event_queryset.filter(service_level="P1", state="ended").count()
    ing_p1_event = event_queryset.exclude(service_level="P1", state="ended").count()

    print(req_count, incident_count, done_event_count, ing_event_count)

    message_alert_queryset = MessageAlert.objects.filter(
        user=request.user,
        checked=0,
    )
    message_alert_count = message_alert_queryset.count()

    if request.method == "POST":
        pass
    else:
        return render(request, "sla_event_dash.html", locals())


def sla_change_dash(request):

    page_header = "SLA水平管理-变更分析"

    queryset = Change.objects.all()
    sum_count = queryset.count()
    # 变更量统计
    succ_count = queryset.filter(state="ended").count()
    fail_count = queryset.filter(state="failed").count()

    # 变更类型
    req_type = 10
    incident_type = 40

    reject_count = queryset.filter(state="reject").count()
    ended_count = queryset.filter(state="ended").count()

    message_alert_queryset = MessageAlert.objects.filter(
        user=request.user,
        checked=0,
    )
    message_alert_count = message_alert_queryset.count()

    if request.method == "POST":
        pass
    else:
        return render(request, "sla_change_dash.html", locals())


def sla_issue_dash(request):

    page_header = "SLA水平管理-问题分析"

    queryset = Change.objects.all()
    sum_count = queryset.count()
    # 变更量统计
    req_count = queryset.filter().count()
    incident_count = queryset.filter().count()
    done_event_count = queryset.filter().count()
    ing_event_count = queryset.exclude().count()

    late_event = queryset.filter().count()
    normal_event = queryset.exclude().count()
    done_p1_event = queryset.filter().count()
    ing_p1_event = queryset.exclude().count()

    message_alert_queryset = MessageAlert.objects.filter(
        user=request.user,
        checked=0,
    )
    message_alert_count = message_alert_queryset.count()

    if request.method == "POST":
        pass
    else:
        return render(request, "sla_issue_dash.html", locals())


def sla_release_dash(request):

    page_header = "SLA水平管理-发布分析"

    queryset = Change.objects.all()
    sum_count = queryset.count()
    # 变更量统计
    req_count = queryset.filter().count()
    incident_count = queryset.filter().count()
    done_event_count = queryset.filter().count()
    ing_event_count = queryset.exclude().count()

    late_event = queryset.filter().count()
    normal_event = queryset.exclude().count()
    done_p1_event = queryset.filter().count()
    ing_p1_event = queryset.exclude().count()

    message_alert_queryset = MessageAlert.objects.filter(
        user=request.user,
        checked=0,
    )
    message_alert_count = message_alert_queryset.count()

    if request.method == "POST":
        pass
    else:
        return render(request, "sla_release_dash.html", locals())


def satisfaction_log(request):

    if request.method == "POST":
        form = SatisfactionForm(request.POST)
        if form.is_valid():
            logger.info("满意度数据收敛成功")
            data = form.data
            sati_id = data.get("sati_id")
            comment = data.get("comment")
            content = data.get("content")
            is_ended = data.get("is_ended")
            sati_info = SatisfactionLog.objects.filter(id=int(sati_id), checked=0)
            if not int(is_ended):
                try:
                    sati = sati_info.first().event.state = "processing"
                except Exception as e:
                    logger(e)
            if sati_info:
                sati = sati_info.first()
                sati.comment = comment
                sati.content = content
                sati.checked = 1
                sati.save()
            return HttpResponse("评价成功")
        else:
            logger.info(form.errors)
    else:
        sati_log_id = request.GET.get("log_id")
        print(sati_log_id)
        try:
            sati_info = SatisfactionLog.objects.get(id=sati_log_id, checked=0)
            event = sati_info.event
        except Exception as e:
            logger.info(e)
            return HttpResponse("满意度调查已回复或者不存在")
        form = SatisfactionForm()
        return render(request, "satisfaction.html", locals())