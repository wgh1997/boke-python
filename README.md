# 基于django 开发博客服务端
[前台博客](https://github.com/wgh1997/wangguohui.cn)
[后台博客管理](https://github.com/wgh1997/boke-ui-admin)
## 主要功能：
- [x] 文章，页面，分类目录，标签的添加，删除，编辑等。文章、评论及页面支持Markdown，支持代码高亮。
- [x] 支持文章全文搜索。
- [ ] 完整的评论功能 
- [ ] 支持Oauth登陆
- [ ] 简单的SEO功能，新建文章等会自动通知Google和百度。
- [x] 项目基于Docker启动
- [x] 项目配置Github Actions 自动化部署项目


## 运行项目
运行项目之前要再`/boke-python/boke/`目录下创建`local.py`文件配置es数据库账号密码
```python
from .settings import *
ES_NAME='name'
ES_PASSWOR='123456'
```
```
docker-compose up

```
