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
from member.views import GroupViewSet
from pps.views import ProductViewSet, OrderViewSet
from finance.views import TradingRecordViewSet
from wechat.views import LoginView

schema_view = get_swagger_view(title='Smart PPS Rest API')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^docs', schema_view),
    url(r'^wx_login', LoginView.as_view()),
]

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'groups', GroupViewSet, 'groups')
router.register(r'products', ProductViewSet, 'products')
router.register(r'orders', OrderViewSet, 'orders')
router.register(r'trading_records', TradingRecordViewSet, 'trading_records')

urlpatterns += router.urls
