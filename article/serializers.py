

from rest_framework import serializers
from .models import Article, ClassifyModels, TagsModels, TagsArticleModels
from django_celery_beat.models import CrontabSchedule


class pagingSerializer(serializers.Serializer):
    pageNum = serializers.UUIDField(label='pageNum', error_messages={
        "blank": "标签id不能为空",
        "required": "缺少标签id字段"
    })
    pageSize = serializers.CharField(label='pageSize', error_messages={
        "blank": "标签名称不能为空",
        "required": "缺少标签名称字段"
    })
class TagsSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True, label='标签id', error_messages={
        "blank": "标签id不能为空",
        "required": "缺少标签id字段"
    })
    name = serializers.CharField(label='标签名称', max_length=30, error_messages={
        "blank": "标签名称不能为空",
        "required": "缺少标签名称字段"
    })
    user_id = serializers.UUIDField(label='用户id', write_only=True, error_messages={
        "blank": "用户id不能为空",
        "required": "缺少用户id字段"
    })

    class Meta:
        model = TagsModels

    def create(self, validated_data):
        """新建"""
        print(validated_data, "-->")
        return TagsModels.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """更新，instance为要更新的对象实例"""
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance


class TagsArticleSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True, label='标签id', error_messages={
        "blank": "标签id不能为空",
        "required": "缺少标签id字段"
    })
    article_id = serializers.UUIDField(label='文章id', error_messages={
        "blank": "文章id不能为空",
        "required": "缺少用户id字段"
    })
    tags_id = serializers.UUIDField(label='标签id', error_messages={
        "blank": "标签id不能为空",
        "required": "缺少用户id字段"
    })
    name = serializers.SerializerMethodField()

    class Meta:
        model = TagsArticleModels

    def get_name(self, obj):
        publisher = TagsModels.objects.get(id=obj.tags_id)
        # data = TagsSerializer(publisher, many=True)
        return publisher.name

    def create(self, validated_data):
        """新建"""
        print(validated_data, "-->")
        return TagsArticleModels.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """更新，instance为要更新的对象实例"""
        instance.article_id = validated_data.get(
            'article_id', instance.article_id)
        instance.tags_id = validated_data.get('tags_id', instance.tags_id)
        instance.save()
        return instance


class ArticleSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True, label='id', error_messages={
        "blank": "id不能为空",
        "required": "缺少id字段"
    })
    article_name = serializers.CharField(
        max_length=100,
        required=True,
        label='名称',
        error_messages={
            "blank": "名称不能为空",
            "required": "缺少名称参数"
        })
    user_id = serializers.UUIDField(label='用户id', write_only=True)  # 用户id
    article_topping = serializers.IntegerField(
        default=0,
        label='是否置顶',
        error_messages={
            "blank": "是否置顶不能为空",
            "required": "缺少是否置顶参数"
        })
    article_type = serializers.CharField(label='类型', error_messages={
        "blank": "类型不能为空",
        "required": "缺少类型参数"
    })
    tags = serializers.CharField(label='标签', error_messages={
        "blank": "标签不能为空",
        "required": "缺少标签参数"
    })

    read = serializers.IntegerField(default=0, label='阅读量', error_messages={
        "blank": "阅读量不能为空",
        "required": "缺少阅读量参数"
    })
    revise_time = serializers.DateTimeField(label='修改时间', error_messages={
        "blank": "修改时间不能为空",
        "required": "缺少修改时间参数"
    })
    article_img = serializers.CharField(label='文章图片', error_messages={
        "blank": "文章图片不能为空",
        "required": "缺少文章图片参数"
    })
    article_body = serializers.CharField(label='文章内容', read_only=True, error_messages={
        "blank": "文章内容不能为空",
        "required": "文章内容类型参数"
    })
    create_time = serializers.DateTimeField(label='创建时间', error_messages={
        "blank": "创建时间不能为空",
        "required": "缺少创建时间参数"
    })
    article_tags = serializers.SerializerMethodField()

    class Meta:
        model = Article

    def get_article_tags(self, obj):
        publisher = TagsArticleModels.objects.filter(article_id=obj.id)
        data = TagsArticleSerializer(publisher, many=True)
        return data.data

    def create(self, validated_data):
        """新建"""
        print(validated_data, "-->")
        return Article.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """更新，instance为要更新的对象实例"""
        instance.article_name = validated_data.get(
            'article_name', instance.article_name)
        instance.article_topping = validated_data.get(
            'article_topping', instance.article_topping)
        instance.article_type = validated_data.get(
            'article_type', instance.article_type)
        instance.tags = validated_data.get('tags', instance.tags)
        instance.read = validated_data.get('read', instance.read)
        instance.revise_time = validated_data.get(
            'revise_time', instance.revise_time)
        instance.article_img = validated_data.get(
            'article_img', instance.article_img)
        instance.create_time = validated_data.get(
            'create_time', instance.create_time)
        instance.save()
        return instance


class ArticleBodySerializer(serializers.Serializer):
    id = serializers.UUIDField(label='id', error_messages={
        "blank": "id不能为空",
        "required": "缺少id字段"
    })
    article_body = serializers.CharField(label='文章内容', allow_null=True, error_messages={
        "blank": "文章内容不能为空",
        "required": "文章内容类型参数"
    })

    class Meta:
        model = Article

    def update(self, instance, validated_data):
        """更新，instance为要更新的对象实例"""
        instance.article_body = validated_data.get(
            'article_body', instance.article_body)
        instance.save()
        return instance


class ClassifySerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True, label='id', error_messages={
        "blank": "id不能为空",
        "required": "缺少id字段"
    })  # id
    name = serializers.CharField(label='名称', max_length=30, error_messages={
        "blank": "名称不能为空",
        "required": "缺少名称字段"
    })  # 标题
    user_id = serializers.UUIDField(label='用户id', write_only=True, error_messages={
        "blank": "用户id不能为空",
        "required": "缺少用户id字段"
    })  # 用户id

    class Meta:
        model = ClassifyModels

    def create(self, validated_data):
        """新建"""
        print(validated_data, "-->")
        return ClassifyModels.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """更新，instance为要更新的对象实例"""
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance
# minute：分钟，范围0-59；
# hour：小时，范围0-23；
# day_of_week：星期几，范围0-6。以星期天为开始，即0为星期天。这个星期几还可以使用英文缩写表示，例如“sun”表示星期天；
# day_of_month：每月第几号，范围1-31；
# month_of_year：月份，范围1-12
class TaskSerializer(serializers.Serializer):
    name = serializers.CharField(label='定时任务名称',
                                 error_messages={
                                     "blank": "定时任务名称不能为空",
                                     "required": "缺少定时任务名称参数"
                                 })
    minute = serializers.CharField(label='分钟', write_only=True, default="*",error_messages={
        "blank": "分钟不能为空",
        "required": "缺少分钟参数"
    })
    hour = serializers.CharField(label='小时', write_only=True, default="*", error_messages={
        "blank": "小时不能为空",
        "required": "缺少小时参数"
    })
    day_of_week = serializers.CharField(label='星期几', write_only=True, default="*", error_messages={
        "blank": "星期几不能为空",
        "required": "缺少星期几参数"
    })
    day_of_month = serializers.CharField(label='每月第几号', write_only=True, default="*", error_messages={
        "blank": "每月第几号不能为空",
        "required": "缺少每月第几号参数"
    })
    month_of_year = serializers.CharField(label='月份', write_only=True, default="*", error_messages={
        "blank": "月份不能为空",
        "required": "缺少月份参数"
    })
    enabled = serializers.BooleanField(label='是否开启定时任务', default=False, error_messages={
        "blank": "enabled不能为空",
        "required": "缺少enabled参数"
    })
    crontab_id = serializers.CharField(label='crontab_id',read_only=True)
    crontab = serializers.CharField(label='crontab',read_only=True)
