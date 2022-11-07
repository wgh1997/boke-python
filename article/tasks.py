import traceback
from celery_task.main import app
from boke.es import es, index
from elasticsearch import helpers
from article.models import Article as ArticleModels
from article.serializers import ArticleSerializer

@app.task
def cogradient(*para):
        # 定时从数据库同步到es文章数据
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
        return 'es文章同步成功'