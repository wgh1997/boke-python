import json
import random
from datetime import datetime, timedelta

import pytz
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.core.cache import cache
from django.core.mail import send_mail
from django.http import HttpResponse
# Create your views here.
from django.shortcuts import render
from django_celery_beat.models import (CrontabSchedule, IntervalSchedule,
                                       PeriodicTask, PeriodicTasks)
from django_redis import get_redis_connection
from pytz import timezone
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
# from scipy import rand
from tools.sms import YunTongXin

# from users.captcha import Captcha
from users.captcha import create_captcha

from .models import User
from .tasks import send_sms_celery, timing


class Users(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        if 'username' not in request.data:
            return Response(dict(code=1, msg="请输入用户名"))
        if 'password' not in request.data:
            return Response(dict(code=1, msg="请输入密码"))
        # if 'code' not in request.data:
        #     return Response(dict(code=1, amg="请输入验证码"))
        # if request.session['captcha'] != request.data['code']:
        #     return Response(dict(code=1, amg="图形验证码不正确"))
        username = request.data['username']
        password = request.data['password']
        user = authenticate(username=username, password=password)
        print(request.data)
        if user is not None:
            login(request, user)
            return Response(dict(code=0, message="success", msg="登录成功"))
        else:
            return Response(dict(code=1, message="success", msg="登录失败"))
        # user = User.objects.create_user(username='wgh', password='123', email='00',)
        # user = User.objects.create_superuser(username = 'wangguohui', password = 'wgh123456', email = '111@qq.com')


class Register(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        if 'username' not in request.query_params:
            return Response(dict(code=1, message="请输入用户名"))
        if 'password' not in request.query_params:
            return Response(dict(code=1, message="请输入密码"))
        # if 'email' not in request.query_params:
        #         return Response(dict(code=1, message="请输入邮箱"))

        username = request.query_params['username']
        password = request.query_params['password']
        # email = request.query_params['email']
        Pbbool = User.objects.filter(username=username).exists()
        if Pbbool:
            return Response(dict(code=1, message="success", msg="用户名已存在"))
        else:
            User.objects.create_user(
                username=username, password=password)
            return Response(dict(code=0, message="success", msg="注册成功"))

    # user = User.objects.create_user(username='wgh', password='123', email='00',)
    # user = User.objects.create_superuser(username = 'wangguohui', password = 'wgh123456', email = '111@qq.com')


class Logout(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        logout(request)
        return Response(dict(code=0, message="success", msg="退出成功"))


class Code(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        valid_str, img_data = create_captcha()
        try:
            request.session['captcha'] = valid_str.lower()
            print(valid_str,'验证码')
            return Response(dict(code=0, data=img_data))
            # return HttpResponse("<img src='"+img_data+"'>")
        except Exception as e:
            # logger.error('Refresh captcha error: {}'.format(e))
            return Response(dict(code=1, msg="验证码获取失败"))


class Info(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        return Response(dict(code=0, data={"username": request.user.username})) if request.user.is_authenticated else HttpResponse(status=401)
# 发送邮件
class Email(APIView):
    permission_classes = [AllowAny]

    def email(request):
        msg = '模特图'
        send_mail(
            subject='请注意查收',
            message=msg,
            from_email=settings.EMAIL_HOST_USER,
            # 这里注意替换成自己的目的邮箱，不然就发到我的邮箱来了：）
            recipient_list=["hyianb91526@chacuo.net"]

        )
        return HttpResponse('测试邮件已发出请注意查收')


class PhoneCode(APIView):
    permission_classes = [AllowAny]

    def get(self, request):  # sourcery skip: avoid-builtin-shadow

        # # print(code)
        # cache.set('17635063817',code)
        # print(cache.get('17635063817'),'9090')
        if 'phone' not in request.query_params:
            return Response(dict(code=1, message="请输入手机号"))
        phone = request.query_params['phone']
        if cache.get(phone) is None:
            code = random.randint(1000, 9999)
            # 储存到redis
            cache.set(phone, code, timeout=180)
            # 发送短信
            send_sms_celery.delay(phone, code)
            # list = json.loads(sms)
            # if list['statusCode']=='000000':
            return Response(dict(code=0, msg='验证码发送成功'))
            # else:
            #         cache.set(phone, code, timeout=0)
            #         return Response(dict(code=0, msg='验证码发送失败'))
        else:
            mas = '{"statusCode": "000000", "templateSMS": {"smsMessageSid": "79af2ab44a674f2a86d9c40000f27698", "dateCreated": "20220504193848"}}'
            list = json.loads(mas)
            print(list['statusCode'])
            return Response(dict(code=1, message="请勿重复发送验证码"))


class Timing(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # crontab_time = {
        #         'minute': '*/10',
        #         'hour': '*',
        #         'day_of_week': '*',
        #         'day_of_month': '*',
        #         'month_of_year': '*'
        # }
        # task = 'users.tasks.timing'
        # schedule = CrontabSchedule.objects.update_or_create(**crontab_time)
        # task, created = PeriodicTask.objects.update_or_create(
        # name='test_task',		# 名称保持唯一
        # task=task,
        # crontab=schedule,
        # enabled=True,	# 是否开启
        # # args=json.dumps(task_args)
        # # kwargs=json.dumps(task_kwargs),
        # # expires=datetime.datetime.now()+datetime.timedelta(days=1)	# 过期时间
        # )
        # if created:
        #         return HttpResponse("创建成功")
        # else:
        #         return HttpResponse("创建失败")
        # 修改任务
        # crontab_time = {
        #         'minute': '*/1',
        #         'hour': '*',
        #         'day_of_week': '*',
        #         'day_of_month': '*',
        #         'month_of_year': '*',
        #         'timezone':pytz.timezone("Asia/Shanghai"),
        # }
        # # task = 'users.tasks.timing'
        # schedule, _ = CrontabSchedule.objects.update_or_create(**crontab_time)
        # task = PeriodicTask.objects.filter(name__startswith='test_task').first()

        # task.crontab = schedule
        # task.save()
        # PeriodicTasks.changed(task)
        # if task:
        #         return HttpResponse("修改成功")
        # else:
        #         return HttpResponse("修改失败")
        # 停止任务
        task = PeriodicTask.objects.filter(
            name__startswith='test_task').first()
        if task:
            task.enabled = False
            task.save()
            return HttpResponse("停止成功")
        # 启动任务
        # task = PeriodicTask.objects.filter(name__startswith='test_task').first()
        # if task:
        #         task.enabled=True
        #         task.save()
        #         return HttpResponse("启动成功")
        # 删除任务
        # task = PeriodicTask.objects.filter(name__startswith='test_task')
        # print(task)
        # if task:
        #         task.update(enabled=False)
        #         task.delete()
        #         return HttpResponse("删除成功")
        # crontab, _ = CrontabSchedule.objects.update_or_create(
        #         minute="*/1",
        #         hour="*",
        #         day_of_week="*",
        #         day_of_month='*',
        #         month_of_year='*',
        #         timezone=pytz.timezone("Asia/Shanghai")

        # )

# def send_sms(phone,code):
#         yun = YunTongXin('8aaf0708806f236e01808e3319e00532','89f2b6b1438c4994bec72d05f195a174', '8aaf0708806f236e01808e331ada0539', 1)
#         res = yun.run(phone,code)
#         return res
