from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .service import service_impl as service
from .models import User
import redis
import os
import subprocess

r = redis.Redis(host='localhost', port=6379, decode_responses=True)
qr_path = 'C:/Users/ghj/Desktop/xupt_ghj/static/wx/wx.png'


# Create your views here.
class Control(object):
    def wx_c(self, request):
        if not os.path.exists(qr_path):
            return HttpResponse('ok')
        else:
            return HttpResponse('wait login')

    def wx(self, request):
        return render(request, 'wx.html')

    def wx_login(self, request):
        user = request.session.get('user', None)
        if r.exists(user) and r.get(user):
            out = subprocess.getoutput("ps -ef|grep 'python3 ./wx' | "
                                       "grep -v grep | awk '{print $2}'")
            if len(out) != 0:
                return HttpResponse('already login')
        out = subprocess.getoutput('python3 ./wx.py ' + user)
        if 'Getting uuid of QR code.' in out:
            while not os.path.exists(qr_path):
                pass
            return HttpResponse('ok')
        return HttpResponse('already login')

    def time(self, request):
        return render(request, 'time.html')

    def send(self, request):
        key = request.POST.get('key', None)
        device = request.POST.get('device', None)
        status = service.send(device, key)
        if status:
            return HttpResponse('ok')
        else:
            return HttpResponse('no')

    def use(self, request):
        ctx = {}
        id = request.POST.get('id', None)
        ctx['name'] = service.get_device_name(id)
        ctx['device'] = service.get_device(id)
        type = request.POST.get('type', None)
        ctx['type'] = type
        # some code must be input
        return render(request, 'device.html', ctx)

    def name_change(self, request):
        name = request.GET.get('name', None)
        if name is None:
            return HttpResponse("Name id is NULL！")
        _id = request.GET.get('id', None)
        if _id is None:
            return HttpResponse("Device id is NULL！")
        status = service.change_name(_id, name)
        if status == 1:
            return HttpResponse('ok')
        elif status[0] == 'D':
            return HttpResponse(status)
        else:
            return HttpResponse('change failed:<br>Sql Exception')

    def name_del(self, request):
        _id = request.GET.get('id', None)
        if _id is None:
            return HttpResponse("Device id is NULL！")
        status = service.del_device(_id)[1]['remote_control.Device']
        if status == 1:
            return HttpResponse('ok')
        else:
            return HttpResponse('delete Device：0<br>Sql Exception')

    def name(self, request):
        ctx = {}
        ctx['count'] = service.get_un_naming_count()
        ctx['list'] = service.get_un_naming()
        return render(request, 'unnaming.html', ctx)

    def reset_submit(self, request):
        status = ''
        pwd1 = request.POST.get('pwd1', None)
        pwd2 = request.POST.get('pwd2', None)
        if pwd1 is None or pwd2 is None or pwd1 != pwd2:
            return HttpResponse('null_value')
        mail = request.session.get('mail', None)
        if mail is not None:
            if r.get(mail) == 'true':
                status = service.submit(pwd1, mail)
                r.delete(mail)
                request.session['mail'] = None
        return HttpResponse(status)

    def reset_check(self, request):
        mail = request.POST.get('mail', None)
        code = request.POST.get('code', None)
        num = r.get(mail)
        if code == num:
            r.set(mail, 'true')
            request.session['mail'] = mail
            return HttpResponse('ok')
        else:
            return HttpResponse('验证码错误')

    def create(self, request):
        mail = request.POST.get('mail', None)
        if not service.check(mail):
            return HttpResponse('邮箱输错啦！没有这个用户')
        num = service.create()
        if len(mail) == 0:
            return HttpResponse('网络错误')
        status = service.send_mail(mail, num)
        if status == 'ok':
            try:
                r.set(mail, num, ex=61)
            except:
                return HttpResponse('redis 连接失败')
            return HttpResponse(status)
        else:
            return HttpResponse('无法发送邮件到此用户，自己改数据库吧')

    def reset(self, request):
        return render(request, 'reset_password.html')

    def logout(self, request):
        request.session['user'] = None
        return render(request, 'login.html')

    def login(self, request):
        return render(request, 'login.html')

    def login_check(self, request):
        user_name = request.POST.get('username', None)
        pass_word = request.POST.get('password', None)
        if service.check_login(user_name, pass_word):
            request.session['user'] = user_name
            return HttpResponse('ok')
        return HttpResponse('none')

    def home(self, request):
        ctx = {}
        user = request.session.get('user', None)
        ctx['name'] = User.objects.filter(id=user).values('user_name').get()['user_name']
        ctx['count'] = service.get_un_naming_count()
        return render(request, 'home.html', ctx)

    def mine(self, request):
        ctx = {}
        ctx['count'] = service.get_un_naming_count()
        ctx['list'] = service.get_naming()
        return render(request, 'mine.html', ctx)

    def study_key(self, request):
        key_name = request.GET.get('keyName', None)
        command = request.GET.get('command', None)
        print(key_name, command)
        return HttpResponse('ok')

    def page_not_found(self, request):
        return render(request, '404.html')

    # def page_error(self, request):
    #     return render(request, '500.html')
