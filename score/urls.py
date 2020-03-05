from django.contrib import admin
from django.urls import path
from score import views
app_name = 'score'
urlpatterns = [
    path('admin/', admin.site.urls),
    # 分数查看
    path('score_rank/', views.score_rank, name='score_rank'),
    # 上传分数
    path('score_add/', views.socre, name='score_add'),

    # 注册登录
    path('reg/', views.reg, name='reg'),
    path('login/', views.login, name='login'),
]