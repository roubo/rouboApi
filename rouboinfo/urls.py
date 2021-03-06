"""rouboinfo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include


# 使用URL路由来管理我们的API
# 另外添加登录相关的URL
urlpatterns = [
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    #path('admin/', admin.site.urls),
    url(r'^roubo/rouboapi/', include('rouboapi.urls'))
]
