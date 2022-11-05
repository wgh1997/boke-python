from .local import (
    ES_NAME,
    ES_PASSWOR,
)
from elasticsearch import Elasticsearch
#查看证书位置
import ssl
##忽视证书
context = ssl._create_unverified_context()
name = ES_NAME
password = ES_PASSWOR
ES =["42.192.148.228:9200"]
# 创建elasticsearch客户端
es = Elasticsearch(
    ES,
    http_auth=(name,password),##账号密码
    scheme="http",
    ssl_context=context,
)
index = "bock"
