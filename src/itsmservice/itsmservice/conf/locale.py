# cas conf
SUCC_REDIRECT_URL = "test.itsm.ecscloud.com"
CAS_SERVER_URL = "http://test.cas.ecscloud.com/cas/"
CMP_URL = "http://test.cmp.ecscloud.com"
# CAS_REDIRECT_URL = "http://www.baidu.com"


# databases conf
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'itsm',
        'USER': 'root',
        'PASSWORD': '123123',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
    },
    'cas_db': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'cas',
        'USER': 'root',
        'PASSWORD': '123123qwe',
        "HOST": "111.13.61.167",
        "PORT": "3306",
    },
}
# use multi-database in django
DATABASE_ROUTERS = ['itsmservice.database_router.DatabaseAppsRouter']
DATABASE_APPS_MAPPING = {
    # example:
    # 'app_name':'database_name',
    'cas_sync': 'cas_db',
}


# fit2cloud api conf

CLOUD_HOST = "111.13.61.173"
CMDB_HOST = "111.13.61.173"
access_key = "My00ZjRkMzVkZA=="
cloud_secret_key = "228e1f50-3b39-4213-a8d8-17e8bf2aeb1e"
INTERNET_HOST = "111.13.61.173"

CMDB_CONF = {
    "access_key": access_key,
    "version": "v1",
    "signature_method": "HmacSHA256",
    "signature_version": "v1"
}

CLOUD_CONF = {
    "access_key": access_key,
    "version": "v1",
    "signature_method": "HmacSHA256",
    "signature_version": "v1",
    "user": "sunyaxiong@vstecs.com",
}
secret_key = cloud_secret_key
# cloud_secret_key = '228e1f50-3b39-4213-a8d8-17e8bf2aeb1e'

# mail
EMAIL_HOST = 'smtp.163.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'sunyaxiongnn@163.com'
EMAIL_HOST_PASSWORD = 'Sun880519'
EMAIL_SUBJECT_PREFIX = u'[vstecs.com]'
EMAIL_USE_TLS = True

