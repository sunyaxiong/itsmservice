import logging

from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect

from itsmservice import settings
from apps.accounts.models import Profile, MessageAlert
from apps.knowledges.models import Knowledge
from apps.changes.models import Change
from .models import Issue, IssueProcessLog
from .forms import IssueDetailForm, IssueToKnowForm

logger = logging.getLogger("django")


def issues(request):

    cmp_url = settings.CMP_URL
    page_header = "问题管理"
    data = Issue.objects.filter()
    count = data.count()
    return render(request, "issue_list.html", locals())


def issue_detail(request, pk):
    page_header = "问题管理"
    issue = Issue.objects.get(id=int(pk))
    solution_list = issue.logs.all() if issue.logs else []
    user_list = User.objects.all()
    degree_choice_list = Change.EMERGENCY_DEGREE
    host = settings.INTERNET_HOST

    # 用户\管理员监控url不同
    profile = Profile.objects.filter(username=request.user.username).first()

    # 根据事件状态控制按钮显隐和名称
    button_submit = "保存"
    display = 0 if issue.state == "off" else 1

    if request.method == "GET":

        # 解决方案列表,循环展示
        return render(request, 'issue_detail.html', locals())
    elif request.method == "POST":

        # form收敛数据
        issue_form = IssueDetailForm(request.POST)
        if issue_form.is_valid():
            data = issue_form.data

            if data.get("emergency_degree"):
                issue.emergency_degree = data["emergency_degree"]

            if data.get("handler"):
                tc = User.objects.get(username=data.get("handler"))
                issue.handler = tc

            if data.get("attach_file"):
                issue.attach_file = data.get("attach_file")

            if issue.state == "draft":
                issue.state = "processing"

                # 更新解决方案
            if data.get("solution"):
                IssueProcessLog.objects.create(
                    issue_obj=issue,
                    username=data.get("handler"),
                    content=data.get("solution"),
                )
            issue.save()
            return HttpResponseRedirect("/issues/issue_list/")
        messages.warning(request, issue_form.errors)
        return render(request, 'issue_detail.html', locals())


def issue_close(request, pk):
    url = request.META.get('HTTP_REFERER')
    try:
        issue = Issue.objects.get(id=pk)
        if issue.state == "off":
            messages.warning(request, "当前问题已关闭")
            return HttpResponseRedirect(url)
        if issue.handler_id is not request.user.id:
            messages.warning(request, "您不是当前处理人,无法处理该问题")
            return HttpResponseRedirect(url)

        # 执行关闭
        issue.state = "off"
        issue.save()
        return HttpResponseRedirect(url)
    except Exception as e:
        messages.warning(request, "问题查询异常: {}".format(e))
        return HttpResponseRedirect(url)


def issue_upgrade(request):

    url = request.META.get('HTTP_REFERER')
    username = request.GET.get("username")
    issue_id = request.GET.get("issue_id")
    logging.warning("ajax test: {}: {}: {}".format(url, username, issue_id))

    handler = User.objects.filter(username=username)
    issue = Issue.objects.filter(id=issue_id)[0]
    issue.handler = handler[0]
    issue.save()

    return HttpResponseRedirect(url)


def issue_to_knowledge(request):
    url = request.META.get('HTTP_REFERER')

    if request.method == "POST":
        form = IssueToKnowForm(request.POST, request.FILES)
        if form.is_valid():
            logger.info("问题转换知识库收据收敛成功")
            data = form.cleaned_data
            print("clean_data: ", form.cleaned_data)

            knowledge = Knowledge.objects.create(
                issue_id=data.get("issue_id"),
                issue_name=data.get("issue_name"),
                title=data.get("title"),
                content=data.get("content"),
                attach_file=data.get("attach_file"),
                creater=request.user.username,
                creater_id=request.user.id,
                classify=data.get("classify")
            )

            # 创建消息提醒组织管理员或者系统管理员
            if knowledge:
                try:
                    creater = Profile.objects.get(username=request.user.username)
                    org_admin = Profile.objects.filter(
                        channel_name=creater.channel_name,
                        org_admin=1,
                    ).first()
                    user = User.objects.filter(username=org_admin.username)
                except Exception as e:
                    logger.info("知识库审核消息异常: ", e)
                    user = User.objects.get(username="admin")

                content = "有新的知识库被创建,请审核"
                MessageAlert.objects.create(
                    user=user,
                    initiator=request.user.username,
                    content=content,
                    action_type="knowledge_info",
                )

            return HttpResponseRedirect("/knowledge/knowledge_list/")
        messages.warning(request, form.errors)
        return HttpResponseRedirect(url)
