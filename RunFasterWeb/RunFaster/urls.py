"""RunFaster URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index),
    path('index/reviewReport/<run_id>/', views.reviewReport, name='reviewReport'),
    path('index/runCaseOne/<run_id>/', views.runCaseOne),  # 执行全部用例
    path('index/runCaseAll/', views.runCaseAll),  # 执行全部用例
    path('index/runCaseKeyPre/', views.runCaseKeyPre),  # 执行预发布用例
    path('index/runCaseKeyOnline/', views.runCaseKeyOnline),  # 执行核心用例
    path('index/runMonitor/', views.runMonitor),  # 执行监控
    path('index/stopMonitor/', views.stopMonitor),  # 结束监控
]
