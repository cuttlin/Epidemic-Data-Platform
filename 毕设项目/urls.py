"""毕设项目 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from EDAP import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/',views.hello),
    path('index/',views.index),
    path('service/',views.service),
    path('home/',views.home),
    path('world/',views.world),
    path('worldtrend/',views.worldtrend),
    path('city/',views.city),
    path('chinatrend/',views.chinatrend),
    path('realtime/',views.realtime),
    path('rumor/',views.rumor),
    path('api/',views.api),
    path('api/worldnow/',views.apiworldnow),
    path('api/now/',views.apinow),
    path('api/rumor/',views.apirumors),
    path('api/news/',views.apinews),
]
