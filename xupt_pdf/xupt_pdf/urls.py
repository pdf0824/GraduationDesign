"""xupt_pdf URL Configuration

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
from sign_in_system import tests
from sign_in_system.views import Controller

ct = Controller()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('s/', tests.s),
    path('q/', tests.q),
    path('show/', tests.show),
    path('check_login/', ct.checkUser),
    path('login', ct.login),
    path('logout/', ct.logout),
    path('add', ct.add),
    path('add_face', ct.add_face),
    path('home', ct.home),
    path('attend', ct.attend),
    path('attend/attendList', ct.attendList),
    path('reAttend.do', ct.create_re_attend),
    path('reAttend', ct.reattend),
    path('reAttend/list', ct.re_attend_list),
    path('reAttend/pass', ct.passIn),
    path('reAttend/notPass', ct.notPass),
    path('all', ct.all),
    path('all/list', ct.all_list),
]
