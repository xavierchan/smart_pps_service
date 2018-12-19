"""smart_pps_service URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view

from member.views import UserViewSet, OrganizationViewSet, GroupViewSet
from pps.views import ProductViewSet, OrderViewSet
from blog import views as blog_views
from game.views import GameViewSet
from comic.views import ComicViewSet
from music.views import MusicViewSet
from wechat.views import LoginView
from aliyun_oss import views as aliyun_oss_views
import views

schema_view = get_swagger_view(title='One Service Rest API')

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'articles', blog_views.ArticleViewSet, 'articles')
router.register(r'orgs', OrganizationViewSet, 'orgs')
router.register(r'groups', GroupViewSet, 'groups')
router.register(r'users', UserViewSet, 'users')
router.register(r'products', ProductViewSet, 'products')
router.register(r'orders', OrderViewSet, 'orders')
router.register(r'games', GameViewSet, 'games')
router.register(r'comics', ComicViewSet, 'comics')
router.register(r'musics', MusicViewSet, 'musics')

urlpatterns = [
    url(r'^$', views.index),
    # social
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^blog/', include('blog.urls', namespace='blog')),
    url(r'^game/', include('game.urls', namespace='game')),
    url(r'^ai/', include('ai.urls', namespace='ai')),
    url(r'^comic/', include('comic.urls', namespace='comic')),
    url(r'^music/', include('music.urls', namespace='music')),
    url(r'^crawler', include('crawler.urls')),
    url(r'^manage$', views.manage),
    url(r'^manage/blogs', blog_views.manage),
    url(r'^manage/aliyun_oss', include('aliyun_oss.urls')),
    url(r'^manage/crawler', include('crawler.urls')),
    url(r'^proj$', views.proj),
    url(r'^plan$', views.plan),
    url(r'^about$', views.about),
    url(r'^admin/', admin.site.urls),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^docs', schema_view),
    url(r'^wx_login', LoginView.as_view()),
    # oss
    url(r'^aliyun_oss/', include('aliyun_oss.urls')),
    url(r'^oss_media/(?P<fid>[0-9a-zA-Z\-]+)', aliyun_oss_views.read),
    # url(r'^short_link/', include('short_link.urls')),
    url(r'^api/', include(router.urls)),
    # notifications
    url('^inbox/notifications/', include('notifications.urls', namespace='notifications')),
    # activity
    url(r'^activity/', include('actstream.urls')),
    # account
    # url(r"^account/", include("account.urls")),
    url(r'^mdeditor/', include('mdeditor.urls')),

]
