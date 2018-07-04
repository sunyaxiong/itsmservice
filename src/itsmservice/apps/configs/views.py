import json
import logging

from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from django.contrib import messages
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt

from apps.accounts.models import Profile
from .models import Config

logger = logging.getLogger(__name__)


@csrf_exempt
def config(request):
    url = request.META.get('HTTP_REFERER')

    username = request.user.username

    profile, pf_created = Profile.objects.get_or_create(username=username)
    if profile.channel_name:
        org_name = profile.channel_name
    else:
        org_name = None

    if org_name:
        department_obj, created = Config.objects.get_or_create(name=org_name)
        department_info = department_obj.department

    if request.method == "GET":
        try:
            # 获取配置文件
            res = cache.get("伟仕云安")
            module_name_list = [i["module_name"] for i in res["module_list"]]

            return render(request, 'config.html', locals())
        except Exception as e:
            logger.info(e)
            messages.warning(request, e)
            return render(request, 'config.html', locals())
    elif request.method == "POST":
        data = request.POST
        logger.info("config 收敛成功: ", data)

        # 部门新增逻辑
        if data.get("department"):
            config = Config.objects.get(name=org_name)
            config.department["department"].append(data.get("department"))
            config.save()
            logger.info("部门新增完成")
            return HttpResponseRedirect("/itsm/config/")

        return HttpResponseRedirect("/itsm/config/")


def get_department_name_list(request):
    """
    根据组织名称获取部门名称列表
    :param request:
    :return:
    """
    if request.method == "GET":

        data = request.GET
        org_name = data.get("org_name")
        department = Config.objects.get(name=org_name).department
        return JsonResponse(department)


@csrf_exempt
def config_overview(request):
    url = request.META.get('HTTP_REFERER')

    print(request.user.groups)
    res = cache.get("伟仕云安")
    import pprint
    pprint.pprint(res)
    module_name_list = [i["module_name"] for i in res["module_list"]]
    if request.method == "POST":
        return HttpResponse(json.dumps(module_name_list), content_type='application/json')
