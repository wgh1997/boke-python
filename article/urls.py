
from django.urls import path
from . import views

urlpatterns = [
    path('list', views.Article.as_view()),
    path('list_body', views.ArticleBody.as_view()),
    path('classify', views.Classify.as_view()),
    path('tags', views.Tags.as_view()),
    path('tags_artic', views.TagsArtic.as_view()),
    path('uploadimg', views.UploadImageView.as_view()),
    path('task', views.TaskView.as_view()),
    path('text', views.TextView.as_view()),
    
    
]
