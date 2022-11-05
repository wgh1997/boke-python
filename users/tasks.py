from tools.sms import YunTongXin
from boke.celery_m import app
from .models import User
from django.core.mail import send_mail
from django.conf import settings
@app.task
def send_sms_celery(phone,code):
        yun = YunTongXin('8aaf0708806f236e01808e3319e00532','89f2b6b1438c4994bec72d05f195a174', '8aaf0708806f236e01808e331ada0539', 1)
        return yun.run(phone,code)
@app.task
def timing():
        
        # msg = '服务器运行良好'
        # send_mail(
        #         subject='请注意这是Django邮件测试',
        #         message=msg,
        #         from_email=settings.EMAIL_HOST_USER,
        #         # 这里注意替换成自己的目的邮箱，不然就发到我的邮箱来了：）
        #         recipient_list=["875193607@qq.com"]

        # )
        return '发送成功'