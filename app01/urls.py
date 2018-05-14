"""day27 URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from app01 import views
from django.contrib.auth.views import login, logout

urlpatterns = [
    url(r'^$', views.Login.as_view(),name='index'),
    url(r'^login.html$', views.Login.as_view(), name='login'),
    url(r'^logout.html$', views.LogOut.as_view(),name='logout'),

    url(r'^userinfo.html$', views.UserInfo.as_view(), name='user_info'),
    url(r'^user-json.html$', views.UserJson.as_view(), name='user_json'),
    url(r'^adduser.html$', views.AddUser.as_view(), name='add_user'),

    url(r'^projectmanage.html$', views.ProjectManage.as_view(), name='app_manage'),
    url(r'^project-json.html$', views.ProjectJson.as_view(), name='app_json'),
    url(r'^addproject.html$', views.AddProject.as_view(), name='add_app'),
    url(r'^r_project.html$', views.ReleaseProject.as_view(), name='release_app'),
]
