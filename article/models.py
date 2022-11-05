from django.db import models
import uuid
# Create your models here.


class Article(models.Model):
    GENDER_CHOICES = (
        (0, True),
        (1, False)
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.UUIDField(verbose_name='用户id')  # 用户id
    article_name = models.CharField(max_length=100, verbose_name='名称')
    article_topping = models.SmallIntegerField(
        choices=GENDER_CHOICES, default=0, verbose_name='是否置顶')
    article_type = models.CharField(
        verbose_name='类型', max_length=50, null=True)
    tags = models.TextField(verbose_name='标签', null=True)
    read = models.IntegerField(default=0, verbose_name='阅读量')
    revise_time = models.DateTimeField(verbose_name='修改时间', auto_now_add=True)
    article_img = models.ImageField(verbose_name='文章图片', null=True)
    article_body = models.TextField(verbose_name='文章内容', null=True)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    class Meta:
        db_table = 'article'
        managed = True
        verbose_name = '文章'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.article_name


class ClassifyModels(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          editable=False, verbose_name='id')  # id
    name = models.CharField(max_length=30, verbose_name='名称')  # 标题
    user_id = models.UUIDField(verbose_name='用户id')  # 用户id

    class Meta:
        db_table = 'classify'
        managed = True
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class TagsModels(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          editable=False, verbose_name='id')  # id
    name = models.CharField(max_length=30, verbose_name='名称')  # 标题
    user_id = models.UUIDField(verbose_name='用户id')  # 用户id

    class Meta:
        db_table = 'tags'
        managed = True
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class TagsArticleModels(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          editable=False, verbose_name='id')  # id
    tags_id = models.UUIDField(verbose_name='标签id')  # 标签id
    article_id = models.UUIDField(verbose_name='文章id')  # 文章id
    
    class Meta:
        db_table = 'tags_article'
        managed = True
        verbose_name = '标签文章管理表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.tags_id
    

