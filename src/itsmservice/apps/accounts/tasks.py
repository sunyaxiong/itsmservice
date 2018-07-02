# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives, send_mail
from itsmservice import settings
from .models import Profile
import datetime


@shared_task
def user_check():

    today = datetime.date.today()
    profiles = Profile.objects.all()
    for i in profiles:
        if i.last_reset_pass:
            if today - i.last_reset_pass > datetime.timedelta(days=90):
                send_mail("密码到期提醒",
                    "尊敬的云平台用户您好,您已经超过90天未修改密码,为保证账户安全,"
                    "请尽快修改密码: http://itsm.ecscloud.com",
                    settings.EMAIL_HOST_USER, [i.email])

if __name__ == "__main__":
    user_check()
    print("user_check ok")

