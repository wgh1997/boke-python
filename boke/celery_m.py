from celery import Celery
from celery.schedules import timedelta, crontab
from django.conf import settings
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "boke.settings")
app = Celery('boke')
# app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.update(
    BROKER_URL="redis://127.0.0.1:6379",
    # CELERYBEAT_SCHEDULE={
    #     'task_1': {
    #         'task': 'users.tasks.timing', # 指定任务
    #         'schedule': timedelta(seconds=10), # 每十秒执行一次
    #         'args': (3, 6)  # 参数
    #     },

    # }
)
app.autodiscover_tasks(settings.INSTALLED_APPS)
