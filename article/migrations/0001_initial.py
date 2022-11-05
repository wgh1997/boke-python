# Generated by Django 3.2.4 on 2022-10-17 08:41

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('user_id', models.UUIDField(verbose_name='用户id')),
                ('article_name', models.CharField(max_length=100, verbose_name='名称')),
                ('article_topping', models.SmallIntegerField(choices=[(0, True), (1, False)], default=0, verbose_name='是否置顶')),
                ('article_type', models.CharField(max_length=50, null=True, verbose_name='类型')),
                ('tags', models.TextField(null=True, verbose_name='标签')),
                ('read', models.IntegerField(default=0, verbose_name='阅读量')),
                ('revise_time', models.DateTimeField(auto_now_add=True, verbose_name='修改时间')),
                ('article_img', models.ImageField(null=True, upload_to='', verbose_name='文章图片')),
                ('article_body', models.TextField(null=True, verbose_name='文章内容')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '文章',
                'verbose_name_plural': '文章',
                'db_table': 'article',
                'managed': True,
            },
        ),
    ]
