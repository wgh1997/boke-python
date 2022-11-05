from celery import Celery
from celery.schedules import timedelta, crontab
from kombu import Queue, Exchange
from django.utils import timezone
from django.conf import settings
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "boke.settings")
app = Celery('boke')
# app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.update(
    
    BROKER_URL="redis://redis:6379",
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://redis:6379'),
    CELERY_TIMEZONE='Asia/Shanghai',
    # CELERYBEAT_SCHEDULE={
    #     'task_1': {
    #         'task': 'users.tasks.timing', # 指定任务
    #         'schedule': timedelta(seconds=10), # 每十秒执行一次
    #         'args': (3, 6)  # 参数
    #     },

    # }
    CELERY_QUEUES=(
        Queue('send_msg', Exchange('send_msg'), routing_key='send_msg'),
        Queue('default', Exchange('default'), routing_key='default'),
    ),
    CELERY_DEFAULT_QUEUE='default',
    CELERY_DEFAULT_EXCHANGE='default',
    CELERY_DEFAULT_ROUTING_KEY='default',
    CELERY_ROUTES={
        'celery_task.task.send_email': {'queue': 'send_msg'},
        'celery_task.task.send_iphone': {'queue': 'send_msg'},
        'celery_task.task.send_wx_official_notify': {'queue': 'send_msg'},

        'celery_task.task.export_csv': {'queue': 'default'},
        'celery_task.task.sub': {'queue': 'default'},
        'celery_task.task.update_login_infor': {'queue': 'default'},
    }
)
app.autodiscover_tasks(settings.INSTALLED_APPS)
app.now = timezone.now