
from django.urls import path
from . import views

urlpatterns = [
    path('login', views.Users.as_view()),
    path('register', views.Register.as_view()),
    path('logout', views.Logout.as_view()),
    #captcha //验证码
    path('captcha', views.Code.as_view()),
    path('info', views.Info.as_view()),
    path('email', views.Email.email),
    path('phone_code', views.PhoneCode.as_view()),
    path('timing', views.Timing.as_view()),

]
