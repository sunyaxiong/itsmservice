import time
import logging
import json

from django.http import JsonResponse

from itsmservice import settings
from lib.fit2cloud import Fit2CloudClient

logger = logging.getLogger(__name__)


def get_vm_list(request):

    # 收敛前端提交参数
    param = {
        "cloudAccountId": 1,
        "time_stamp": int(round(time.time() * 1000)),
        "cloud": "aws",
    }

    # 获取vm接口数据
    res = Fit2CloudClient(settings.CMDB_CONF, settings.secret_key).query_vm(param)
    return JsonResponse(res)


def get_disk_list(request):

    # 收敛前端提交参数
    param = {
        "cloudAccountId": 1,
        "time_stamp": int(round(time.time() * 1000)),
        "cloud": "aws",
    }

    # 获取disk接口数据
    res = Fit2CloudClient(settings.CMDB_CONF, settings.secret_key).query_disk(param)
    return JsonResponse(res)


def get_disk_list(request):

    # 收敛前端提交参数
    param = {
        "cloudAccountId": 1,
        "time_stamp": int(round(time.time() * 1000)),
        "cloud": "aws",
    }

    # 获取disk接口数据
    res = Fit2CloudClient(settings.CMDB_CONF, settings.secret_key).query_disk(param)
    return JsonResponse(res)


def get_product_list(request):

    # 工作空间接口请求
    param = {
        "time_stamp": int(round(time.time() * 1000)),
    }
    ak, sk = Fit2CloudClient(
        settings.CLOUD_CONF, settings.cloud_secret_key
    ).get_work_space(param)
    logging.error("ak, sk: ", ak, sk)

    # 打包生成的ak\sk
    if ak and sk:
        _param = {
            "currPage": 1,
            "pageSize": 1000,
            "time_stamp": int(round(time.time() * 1000)),
        }
        _conf = settings.CLOUD_CONF.copy()
        _conf["access_key"] = ak

        res = Fit2CloudClient(
            _conf, sk
        ).get_product_list(_param)
        return JsonResponse(res)
    logging.error("not product list")
    return JsonResponse({
        "code": "1001",
        "msg": "not product list"
    })


def get_cluster_list(request):

    # 工作空间接口请求
    param = {
        "time_stamp": int(round(time.time() * 1000)),
    }
    ak, sk = Fit2CloudClient(
        settings.CLOUD_CONF, settings.cloud_secret_key
    ).get_work_space(param)
    logging.error("ak, sk: ", ak, sk)

    if ak and sk:
        _param = {
            # "currPage": 1,
            # "pageSize": 1000,
            "time_stamp": int(round(time.time() * 1000)),
        }
        _conf = settings.CLOUD_CONF.copy()
        _conf["access_key"] = ak

        res = Fit2CloudClient(_conf, sk).get_cluster_list(_param)

        return JsonResponse(res)

    logging.error("not cluster list")
    return JsonResponse({
        "code": "1001",
        "msg": "not cluster list"
    })


def get_cluster_role_list(request):

    # 工作空间接口请求
    param = {
        "time_stamp": int(round(time.time() * 1000)),
    }
    ak, sk = Fit2CloudClient(
        settings.CLOUD_CONF, settings.cloud_secret_key
    ).get_work_space(param)
    # logging.error("ak, sk: ", ak, sk)

    if ak and sk:
        _param = {
            # "currPage": 1,
            # "pageSize": 1000,
            "clusterId": 1,
            "time_stamp": int(round(time.time() * 1000)),
        }
        _conf = settings.CLOUD_CONF.copy()
        _conf["access_key"] = ak

        res = Fit2CloudClient(_conf, sk).get_cluster_role_list(_param)

        return JsonResponse(res)

    logging.error("not cluster role list")
    return JsonResponse({
        "code": "1001",
        "msg": "not cluster role list"
    })


def order_create(request):

    param = {
        "time_stamp": int(round(time.time() * 1000)),
    }

    post = {
        "clusterRoleId": 2,
        "count": 1,
        "description": "需要机器配置：1c1g",
        "expireTime": 1518451199999,
        "installAgent": True,
        "productId": "c8509c0d-e518-4532-90d9-be8b840b1fc9"
    }

    # 工作空间接口请求
    ak, sk = Fit2CloudClient(
        settings.CLOUD_CONF, settings.cloud_secret_key
    ).get_work_space(param)
    print("ak, sk : ", ak, sk)

    if ak and sk:
        _param = {
            # "time_stamp": int(round(time.time() * 1000)),
            "time_stamp": 1517905240318,
        }
        _conf = settings.CLOUD_CONF.copy()
        _conf["access_key"] = ak
        print("_conf: ", _conf)
        res = Fit2CloudClient(_conf, sk).order_create(_param, json.dumps(post))

        return JsonResponse(res)

    logging.error("not cluster create")
    return JsonResponse({
        "code": "1001",
        "msg": "not order create"
    })


def order_get(request):

    param = {
        "time_stamp": int(round(time.time() * 1000)),
    }

    ak, sk = Fit2CloudClient(
        settings.CLOUD_CONF, settings.cloud_secret_key
    ).get_work_space(param)

    if ak and sk:
        _param = {
            "orderId": request.GET.get("order_id"),
            "time_stamp": int(round(time.time() * 1000)),
            # "time_stamp": 1517905240318,
        }
        _conf = settings.CLOUD_CONF.copy()
        _conf["access_key"] = ak
        _res = Fit2CloudClient(_conf, sk).order_get(_param)
        print(_res["success"])
        if _res["success"]:
            res = {
                "status": _res.get("data")["status"],
            }
        else:
            res = {
                "status": "NONE",
            }

        return JsonResponse(res)


def user_get(request):
    param = {
        "time_stamp": int(round(time.time() * 1000)),
    }
    _conf = settings.CLOUD_CONF.copy()
    _conf.pop("user")
    client = Fit2CloudClient(_conf, settings.cloud_secret_key)
    res = client.user_get(param)

    return JsonResponse(res)


def get_instance_list(request):

    param = {
        "time_stamp": int(round(time.time() * 1000)),
        "currPage": 1,
        "pageSize": 500,
    }
    _conf = settings.CLOUD_CONF.copy()
    _conf.pop("user")
    client = Fit2CloudClient(_conf, settings.cloud_secret_key)
    res = client.get_instance_list(param)

    return JsonResponse(res)


def resource_info(request):

    param = {
        "time_stamp": int(round(time.time() * 1000)),
        "currPage": 1,
        "pageSize": 500,
    }
    _conf = settings.CLOUD_CONF.copy()
    _conf.pop("user")
    client = Fit2CloudClient(_conf, settings.cloud_secret_key)
    res = client.get_instance_list(param)
    data = res.get("data")
    instance_list = data.get("items")
    instance_info = {i["id"]: i for i in instance_list}

    if request.method == "GET":
        instance_id = int(request.GET.get("instance_id"))
        ret = {
            "hostname": instance_info[instance_id].get("hostname"),
            "localIp": instance_info[instance_id].get("localIp"),
            "groupEnvName": instance_info[instance_id].get("groupEnvName"),
            "instanceType": instance_info[instance_id].get("instanceType"),
        }
        return JsonResponse(ret)
