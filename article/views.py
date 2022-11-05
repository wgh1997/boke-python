import os
import traceback
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .serializers import ArticleSerializer, ClassifySerializer, TagsSerializer, ArticleBodySerializer, TagsArticleSerializer, TaskSerializer, pagingSerializer
from .models import Article as ArticleModels, ClassifyModels, TagsModels, TagsArticleModels
from utils.uploads import getNewName
from django.conf import settings
from rest_framework.pagination import PageNumberPagination
from celery_task.articletask import get_article_task, delete_article_task, start_article_task, stop_article_task
from django_celery_beat.models import PeriodicTask
from boke.es import es, index
from elasticsearch import helpers


class StandardPageNumberPagination(PageNumberPagination):
    page_query_param = 'pageNum'
    page_size_query_param = 'pageSize'
    max_page_size = 100
# Create your views here.


class Article(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        try:
            article = ArticleModels.objects.all()
            serializer = ArticleSerializer(article, many=True)
            pagination_class = StandardPageNumberPagination()
            ret = pagination_class.paginate_queryset(serializer.data, request)

        except:
            s = traceback.format_exc()
            print("文章查询失败, msg: --> {}".format(s))
            return Response(dict(code=1, msg="文章查询失败!"))
        return Response(dict(code=0, message="success", data={
            'datalist': ret,
            "total": len(serializer.data)
        }))

    def post(self, request):
        current_user = request.user
        data = request.data
        data['user_id'] = current_user.id
        try:
            serializer = ArticleSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except:
            s = traceback.format_exc()
            print("添加文章失败, msg: --> {}".format(s))
            return Response(dict(code=1, msg="添加文章失败!"))
        return Response(dict(code=0, message="success", msg="添加文章成功"))

    def put(self, request):
        try:
            classify = ArticleModels.objects.get(id=request.data['id'])
            current_user = request.user
        except:
            s = traceback.format_exc()
            print("修改文章失败, msg: --> {}".format(s))
            return Response(dict(code=1, message="success", msg="修改失败"))
        else:
            data = request.data
            data['user_id'] = current_user.id
            serializer = ArticleSerializer(classify, data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(dict(code=0, msg='修改成功'))

    def delete(self, request):
        if 'id' in request.query_params:
            id = request.query_params['id']
            try:
                ArticleModels.objects.filter(id=id).delete()
            except:
                s = traceback.format_exc()
                print("删除文章失败, msg: --> {}".format(s))
                return Response(dict(code=1, msg='删除失败'))
            else:
                return Response(dict(code=0, msg='删除成功'))
        else:
            return Response(dict(code=1, msg='缺少参数'))


class ArticleBody(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        data = request.data
        current_user = request.user
        data['user_id'] = current_user.id
        try:
            classify = ArticleModels.objects.get(id=request.data['id'])
            print(classify.user_id, current_user.id)
            if classify.user_id == current_user.id:
                serializer = ArticleBodySerializer(classify, data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
            else:
                return Response(dict(code=1, message="success", msg="修改失败"))

        except:
            s = traceback.format_exc()
            print("修改文章失败, msg: --> {}".format(s))
            return Response(dict(code=1, message="success", msg="修改失败"))
        return Response(dict(code=0, msg='修改成功'))


class Classify(APIView):
    """
    文章分类
    """
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        current_user = request.user
        try:
            # classify = ClassifyModels.objects.filter(user_id=current_user.id)
            classify = ClassifyModels.objects.all()
            serializer = ClassifySerializer(classify, many=True)
            if request.query_params.get('pageNum', None) is None:
                return Response(dict(code=0, data={'datalist': serializer.data}))
            pagination_class = StandardPageNumberPagination()
            ret = pagination_class.paginate_queryset(serializer.data, request)
        except:
            s = traceback.format_exc()
            print("查询文章失败, msg: --> {}".format(s))
            return Response(dict(code=1, message="success", msg="查询失败"))
        return Response(dict(code=0, data={'datalist': ret, "total": len(serializer.data)}))

    def post(self, request):
        current_user = request.user
        data = request.data
        data['user_id'] = current_user.id
        serializer = ClassifySerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(dict(code=0, msg='添加成功'))

    def put(self, request):
        try:
            classify = ClassifyModels.objects.get(id=request.data['id'])
            current_user = request.user
        except BaseException:
            return Response(dict(code=1, message="success", msg="修改失败"))
        else:
            data = request.data
            data['user_id'] = current_user.id
            serializer = ClassifySerializer(classify, data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(dict(code=0, msg='修改成功'))

    # sourcery skip: avoid-builtin-shadow, remove-unnecessary-else, swap-if-else-branches
    def delete(self, request):
        if 'id' in request.query_params:
            id = request.query_params['id']
            try:
                ClassifyModels.objects.filter(id=id).delete()
            except BaseException:
                return Response(dict(code=1, msg='修改失败'))
            else:
                return Response(dict(code=0, msg='修改成功'))
        else:
            return Response(dict(code=1, msg='缺少参数'))


class Tags(APIView):
    """
    标签分类
    """
    permission_classes = [IsAdminUser]

    def get(self, request):
        current_user = request.user
        classify = TagsModels.objects.filter(user_id=current_user.id)
        serializer = TagsSerializer(classify, many=True)
        if request.query_params.get('pageNum', None) is None:
            return Response(dict(code=0, data={'datalist': serializer.data}))
        pagination_class = StandardPageNumberPagination()
        ret = pagination_class.paginate_queryset(serializer.data, request)
        return Response(dict(code=0, data={
            'datalist': ret,
            "total": len(serializer.data)
        }
        ))

    def post(self, request):
        current_user = request.user
        data = request.data
        data['user_id'] = current_user.id
        serializer = TagsSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(dict(code=0, msg='添加成功'))

    def put(self, request):
        try:
            classify = TagsModels.objects.get(id=request.data['id'])
            current_user = request.user
        except BaseException:
            return Response(dict(code=1, message="success", msg="修改失败"))
        else:
            data = request.data
            data['user_id'] = current_user.id
            serializer = TagsSerializer(classify, data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(dict(code=0, msg='修改成功'))

    # sourcery skip: avoid-builtin-shadow, remove-unnecessary-else, swap-if-else-branches
    def delete(self, request):
        if 'id' in request.query_params:
            id = request.query_params['id']
            try:
                TagsModels.objects.filter(id=id).delete()
            #     ArticleModels.objects.filter(classify_id=id).delete()
            except BaseException:
                return Response(dict(code=1, msg='修改失败'))
            else:
                return Response(dict(code=0, msg='修改成功'))
        else:
            return Response(dict(code=1, msg='缺少参数'))


class TagsArtic(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        if 'article_id' not in request.query_params:
            return Response(dict(code=1, msg='缺少参数'))
        article_id = request.query_params['article_id']
        try:
            data = TagsArticleModels.objects.filter(article_id=article_id)
            serializer = TagsArticleSerializer(data, many=True)
        except:
            s = traceback.format_exc()
            print(f"查询失败, msg: --> {s}", article_id)
        else:
            return Response(dict(code=0, message="success", data={'datalist': serializer.data}))

    def post(self, request):
        data = request.data
        try:
            serializer = TagsArticleSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except Exception:
            s = traceback.format_exc()
            print(f"添加失败, msg: --> {s}")
            return Response(dict(code=1, msg="添加失败!"))
        return Response(dict(code=0, message="success", msg="添加成功"))

    def put(self, request):  # sourcery skip: avoid-builtin-shadow
        if 'id' not in request.query_params:
            return Response(dict(code=1, msg='缺少参数'))
        id = request.query_params['id']
        try:
            classify = TagsArticleModels.objects.get(id=id)
        except Exception:
            s = traceback.format_exc()
            print(f"修改失败, msg: --> {s}")
            return Response(dict(code=1, message="success", msg="修改失败"))
        else:
            data = request.data
            serializer = TagsArticleSerializer(classify, data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(dict(code=0, msg='修改成功'))

    def delete(self, request):  # sourcery skip: avoid-builtin-shadow
        if 'id' not in request.query_params:
            return Response(dict(code=1, msg='缺少参数'))
        id = request.query_params['id']
        try:
            TagsArticleModels.objects.filter(id=id).delete()
        except Exception:
            s = traceback.format_exc()
            print(f"删除文章失败, msg: --> {s}")
            return Response(dict(code=1, msg='删除失败'))
        else:
            return Response(dict(code=0, msg='删除成功'))


class UploadImageView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        """
        上传图片
        @param request:
        @return:
        """
        if image := request.FILES.get('file', None):
            file_info, suffix = os.path.splitext(image.name)
            # 修改照片名称 按需求来进行改写
            image.name = getNewName('avatar') + suffix
            if suffix.upper() not in ['.JPG', '.JPEG', '.PNG']:
                return Response(dict(code=1, msg="照片格式只支持PNG、JPEG、JPG!"))
            path = '%s/%s' % (settings.MEDIA_ROOT, image.name)
            # path = settings.BASE_DIR + '/media/'
            content = image.chunks()
            with open(path, 'wb') as f:
                for i in content:
                    f.write(i)
        return Response(dict(code=0, message="success", data={'fileUrl': f'/media/{image.name}'}))


class TaskView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        try:
            article = PeriodicTask.objects.all()
            serializer = TaskSerializer(article, many=True)
            pagination_class = StandardPageNumberPagination()
            ret = pagination_class.paginate_queryset(serializer.data, request)
        except:
            s = traceback.format_exc()
            print("查询失败, msg: --> {}".format(s))
            return Response(dict(code=1, msg="查询失败!"))
        return Response(dict(code=0, message="success", data={'datalist': ret, "total": len(serializer.data)}))

    def post(self, request):
        try:
            data = request.data
            serializer = TaskSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            get_article_task(data)
        except:
            s = traceback.format_exc()
            print("添加失败, msg: --> {}".format(s))
            return Response(dict(code=1, message="success", msg="添加失败"))

        return Response(dict(code=0, message="success", msg="添加成功"))

    def delete(self, request):
        if 'name' in request.query_params:
            name = request.query_params['name']
            try:
                delete_article_task(name)
            except BaseException:
                return Response(dict(code=1, msg='修改失败'))
            else:
                return Response(dict(code=0, msg='修改成功'))
        else:
            return Response(dict(code=1, msg='缺少参数'))

    def put(self, request):
        if 'enabled' not in request.data:
            return Response(dict(code=1, msg='缺少enabled字段'))
        if 'name' not in request.data:
            return Response(dict(code=1, msg='缺少订阅名称'))
        try:
            data = request.data
            if data['enabled']:
                start_article_task(data['name'])
            else:
                stop_article_task(data['name'])
        except:
            s = traceback.format_exc()
            print("修改失败, msg: --> {}".format(s))
            return Response(dict(code=1, message="success", msg="修改失败"))

        return Response(dict(code=0, message="success", msg="修改成功"))


class TextView(APIView):
    permission_classes = [AllowAny]
    # 最近添加 lately 根据id查询详情id    根据分类id查询 article_type
    def get(self, request):
        pageSize = request.query_params['pageSize']
        pageNum = request.query_params['pageNum']
        query = {
            "match_all": {}
        }
        sort = [
            {
                "article_topping": {
                    "order": "asc"
                }
            },
            {
                "create_time": {
                    "order": "desc"
                }
            }
        ]
        if 'key' in request.query_params:
            key = request.query_params['key']
            query = {
                "multi_match": {
                    "query": key,
                    "fields": ["article_tags", "article_name", "article_body"],
                }
            }
        if 'lately' in request.query_params:
            sort = [
                {
                    "create_time": {
                        "order": "desc"
                    }
                }
            ]
        if 'id' in request.query_params:
            id = request.query_params['id']
            query = {
                "match": {
                    "id.keyword": id,
                }
            }   
        if 'article_type' in request.query_params:
            article_type = request.query_params['article_type']
            query = {
                "match": {
                    "article_type.keyword": article_type,
                }
            }   
        body = {
            "query": query,
            "size": int(pageSize)*int(pageNum),
            "from": int(pageNum)-1,
            "sort": sort
        }
        try:
            datalist = []
            data = es.search(index=index, body=body)
            total = data['hits']['total']['value']
            datalist.extend({**name['_source']} for name in data['hits']['hits'])
        except:
            s = traceback.format_exc()
            print("查询失败, msg: --> {}".format(s))
            return Response(dict(code=1, message="success", msg="查询失败"))
        #es.search(index=index, body=body)
        # return Response(dict(code=0, message="success", data=data))
        return Response(dict(code=0, message="success", data={
            'datalist': datalist,
            "total": total
        }))

    def post(self, request):
        try:
            article = ArticleModels.objects.all()
            serializer = ArticleSerializer(article, many=True)
        except:
            s = traceback.format_exc()
            print(f"文章查询失败, msg: --> {s}")
        print(f"文章查询成功, msg: --> {serializer.data}")
        action = [{
            "_index": index,
            "_id":i['id'],
            "_type": "doc",
            "_source": i
        }for i in serializer.data]
        try:
            helpers.bulk(es, action)
        except:
            s=traceback.format_exc()
            print(f"文章查询失败, msg: --> {s}")
        return Response(dict(code=1, message="success", msg="查询失败"))