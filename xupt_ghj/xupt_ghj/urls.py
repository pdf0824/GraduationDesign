"""xupt_ghj URL Configuration

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
from remote_control.views import Control
from django.views import static
from django.conf import settings

ct = Control()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login', ct.login),
    path('login/check', ct.login_check),
    path('home', ct.home),
    path('mine', ct.mine),
    path('logout', ct.logout),
    path('studyKey', ct.study_key),
    path('reset', ct.reset),
    path('reset.create', ct.create),
    path('reset.check', ct.reset_check),
    path('reset.submit', ct.reset_submit),
    path('name', ct.name),
    path('name.del', ct.name_del),
    path('name.change', ct.name_change),
    path('use', ct.use),
    path('send', ct.send),
    path('time', ct.time),
    path('wxLogin', ct.wx_login),
    path('wx.r', ct.wx),
    path('wx.c', ct.wx_c),
]
