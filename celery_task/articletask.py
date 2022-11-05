import json
from django_celery_beat.models import CrontabSchedule, IntervalSchedule, PeriodicTask, PeriodicTasks
import pytz

def get_article_task(obj):
    print(obj['enabled'])
    crontab_time = {'minute': obj['minute'], 'hour': obj['hour'],
                    'day_of_week': obj['day_of_week'], 'day_of_month': obj['day_of_month'], 'month_of_year': obj['month_of_year']}
    task = 'article.tasks.cogradient'
    schedule,_ = CrontabSchedule.objects.get_or_create(**crontab_time)
    
    data = PeriodicTask.objects.create(
        name=obj['name'],  # 名称保持唯一
        task=task,
        crontab=schedule,
        args=json.dumps([10, 2, 76]),
        enabled=obj['enabled'],  # 是否开启
    )
    return data


def set_article_task():
    crontab_time = {'minute': '*/1','hour': '*','day_of_week': '*','day_of_month': '*','month_of_year': '*','timezone': pytz.timezone("Asia/Shanghai")}
    schedule, _ = CrontabSchedule.objects.update_or_create(**crontab_time)
    task = PeriodicTask.objects.filter(name__startswith='test_task').first()
    task.crontab = schedule
    task.save()
    PeriodicTasks.changed(task)
    return task


def start_article_task(name):
    """
    启动
    """
    task = PeriodicTask.objects.filter(name__startswith=name).first()
    if task:
        task.enabled = True
        task.save()
        return


def stop_article_task(name):
    """
    停止
    """
    task = PeriodicTask.objects.filter(name__startswith=name).first()
    if task:
        task.enabled = False
        task.save()
        return


def delete_article_task(name):
    """
    删除
    """
    task = PeriodicTask.objects.filter(name__startswith=name)
    if task:
        task.update(enabled=False)
        task.delete()
        return
