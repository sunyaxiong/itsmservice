import logging
import requests
import json
import urllib.parse as urllib

from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import auth,messages
from django.contrib.auth.decorators import login_required

from .forms import UserForm
from .forms import ProfileForm, PassResetForm
from .models import Profile, MessageAlert
from apps.cas_sync import models as cas_model
from itsmservice import settings

logger = logging.getLogger("django")


def index(request):
    return render(request, 'index.html')


def login(request):
    if request.method == 'GET':
        form = UserForm()
        return render(request, "login.html")
    else:
        form = UserForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            # user = auth.authenticate(username=username, password=password)
            attrs = {
                "service": "http://{}".format(settings.SUCC_REDIRECT_URL)
            }
            url_attrs = urllib.urlencode(attrs)
            print(settings.SUCC_REDIRECT_URL)
            print(url_attrs)
            cas_login_url = "{}login?{}".format(
                settings.CAS_SERVER_URL, url_attrs
            )

            post_data = {
                "username": username,
                "password": password,
            }
            res = requests.post(cas_login_url, json.dumps(post_data))
            print(dir(res))
            print(res.status_code)

            # return JsonResponse({})
            return HttpResponseRedirect("/")

        else:
            return render(request, "login.html")


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/accounts/login/")


def user_profile(request):
    user = request.user
    url = request.META.get("HTTP_REFERER")

    profile, profile_created = Profile.objects.get_or_create(username=user.username)

    if request.method == "POST":
        if request.POST.get("destroy"):

            # 用户销毁
            username = request.user.username
            try:
                cas_user = cas_model.app_user.objects.using("cas_db").get(username=username)
                cas_user.delete(using="cas_db")
            except Exception as e:
                logger.info("cas用户: {} 删除异常".format(username), e)
            return HttpResponseRedirect("/accounts/logout/")
        form = ProfileForm(request.POST)
        if form.is_valid():
            data = form.data
            email = data.get("email")
            phone = data.get("phone")
            profile.email = email
            profile.phone = phone
            profile.save()
            return HttpResponseRedirect(url)
        else:
            messages.warning(request, "数据收敛失败")
            return HttpResponseRedirect(url)
    else:
        if profile_created:
            messages.warning(request, "用户配置文件自动创建,请维护具体信息")
        form = ProfileForm()
        return render(request, "user_profile.html", locals())


def pwd_restet(request):
    """
    cas密码修改
    :param request:
    :return:
    """
    url = request.META.get("HTTP_REFERER")
    username = request.user.username

    if request.method == "POST":
        form = PassResetForm(request.POST)
        if form.is_valid():
            data = form.data
            try:
                user = cas_model.app_user.objects.using("cas_db").get(
                    username=username,
                )
                user.password = data.get("password")
                user.save(using="cas_db")
                return HttpResponseRedirect("/accounts/logout/")
            except Exception as e:
                logger.info(e)
                messages.warning(request, "用户不存在")
                return HttpResponseRedirect(url)
        else:
            logger.info("密码修改数据提交失败")
            messages.warning(request, "密码提交失败,请重试")
            return HttpResponseRedirect("url")


def user_confirm(request, pk):
    page_header = "新用户审核"
    confirm_message = MessageAlert.objects.get(id=int(pk))
    content_list = confirm_message.content.split("-")
    org, department, username = content_list[0], content_list[1], content_list[2]
    profile = Profile.objects.filter(username=username).first()

    if request.method == "GET":

        return render(request, 'itsm/user_info_confirm.html', locals())
    elif request.method == "POST":
        pass
        return render(request, 'itsm/issue_detail.html', locals())


def user_confirm_accept(request):

    message_id = request.GET.get("id")
    try:
        message_info = MessageAlert.objects.get(id=int(message_id))

        # 用户激活
        user = User.objects.get(username=message_info.initiator)
        user.is_active = 1
        user.is_staff = 1
        user.save()

        # 消息查阅
        message_info.checked = 1
        message_info.save()

        # cas 用户创建逻辑放到审核消息
        cas_user, _ = cas_model.app_user.objects.using("cas_db").get_or_create(
            username=user.username,
        )
        if _:
            cas_user.password = user.password
            cas_user.save(using="cas_db")
            logger.info("CAS用户: {} 注册成功".format(cas_user.username))

        logger.info("用户信息审核成功")
        return HttpResponseRedirect("/itsm/event_list/")
    except Exception as e:
        logger.info(e, "用户信息审核失败")
        messages.warning(request, "用户信息审核失败")
        return HttpResponseRedirect("/itsm/event_list/")


def user_confirm_reject(request):
    url = request.META.get('HTTP_REFERER')

    message_id = request.GET.get("message_id")
    try:
        message_info = MessageAlert.objects.get(id=message_id)

        # 消息查阅
        message_info.checked = 1
        message_info.save()

    except Exception as e:
        logger.info(e)
        return HttpResponseRedirect(url)