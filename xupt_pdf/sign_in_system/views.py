import traceback

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from sign_in_system.service import service
import base64
import os
from .models import QueryCondition
from .models import ReAttend
from .models import Person

# Create your views here.
class Controller:
    def all_list(self, request):
        range_date = request.GET['rangeDate']
        range_date = request.GET['rangeDate']
        class_name = request.GET['className']
        page_size = request.GET['pageSize']
        start = request.GET['start']
        current_page = request.GET['currentPage']
        id = request.session.get('user', None)
        condition = QueryCondition(id=id, range_date=range_date, class_name=class_name)
        condition.set_page_size(page_size)
        condition.set_current_page(current_page)
        condition.set_start_date(range_date.split('/')[0])
        condition.set_end_date(range_date.split('/')[1])
        condition.set_start_row(start)
        # print(condition)
        result = service.get_all_list(condition)
        return HttpResponse(result)

    def all(self, request):
        ctx = {}
        id = request.session.get('user', None)
        ctx['count'] = 0
        if id == '06141083':
            ctx['count'] = service.get_msg_count()
        ctx['img'] = '../static/img/' + id + '.jpg'
        return render(request, 'all.html', ctx)

    def passIn(self, request):
        id = request.GET['id']
        msg = service.pass_re_attend(id)
        return HttpResponse(msg)

    def notPass(self, request):
        id = request.GET['id']
        msg = service.not_pass_re_attend(id)
        return HttpResponse(msg)

    def re_attend_list(self, request):
        id = request.session.get('user', None)
        ctx = {}
        ctx['img'] = '../static/img/' + id + '.jpg'
        ctx['count'] = 0
        if id == '06141083':
            ctx['count'] = service.get_msg_count()
            attend_list = service.get_re_attend_list()
            ctx['list'] = attend_list
            return render(request, 'reAttendApprove.html', ctx)
        else:
            li = service.get_user(id)
            ctx['li'] = li
            return render(request, 'no_permission.html', ctx)

    def reattend(self, request):
        ctx = {}
        id = request.session.get('user', None)
        ctx['count'] = 0
        if id == '06141083':
            ctx['count'] = service.get_msg_count()
        ctx['img'] = '../static/img/' + id + '.jpg'
        li = service.get_re_attend(id)
        ctx['li'] = li
        return render(request, 'reAttend.html', ctx)

    def create_re_attend(self, request):
        re_attend = ReAttend()
        try:
            re_attend.attend_status = request.GET['attendStatus']
            re_attend.attend_date = request.GET['attendDate']
            re_attend.stu_no = request.GET['userID']
            if ReAttend.objects.filter(attend_date=re_attend.attend_date, attend_status=re_attend.attend_status,
                                       stu_no=re_attend.stu_no).exists():
                return HttpResponse('exits')
            re_attend.comments = request.GET['remark']
            re_attend.re_attend_starter = Person.objects.filter(stu_no=request.GET['userID']).values('stu_name')[0][
                'stu_name']
            re_attend.current_handler = '彭大富'
            print(re_attend.attend_date)
            re_attend.save()
        except Exception:
            print(traceback.print_exc())
            return HttpResponse('error')
        return HttpResponse('ok')

    def attendList(self, request):
        range_date = request.GET['rangeDate']
        page_size = request.GET['pageSize']
        start = request.GET['start']
        current_page = request.GET['currentPage']
        id = request.session.get('user', None)
        condition = QueryCondition(id=id, range_date=range_date, class_name="")
        condition.set_page_size(page_size)
        condition.set_current_page(current_page)
        condition.set_start_date(range_date.split('/')[0])
        condition.set_end_date(range_date.split('/')[1])
        condition.set_start_row(start)
        result = service.get_list(condition)
        print(result)
        return HttpResponse(result)

    def attend(self, request):
        ctx = {}
        id = request.session.get('user', None)
        ctx['count'] = 0
        if id == '06141083':
            ctx['count'] = service.get_msg_count()
        ctx['img'] = '../static/img/' + id + '.jpg'
        return render(request, 'attend.html', ctx)

    def home(self, request):
        ctx = {}
        id = request.session.get('user', None)
        ctx['count'] = 0
        if id == '06141083':
            ctx['count'] = service.get_msg_count()
        li = service.get_user(id)
        ctx['li'] = li
        ctx['img'] = '../static/img/' + id + '.jpg'
        return render(request, 'home.html', ctx)

    def logout(self, request):
        request.session['user'] = None
        return render(request, 'login.html')

    def login(self, request):
        return render(request, 'login.html')

    def checkUser(self, request):
        img = request.POST.get('img', None)
        if img is None:
            name = request.POST.get('username', None)
            pwd = request.POST.get('password', None)
            if name is None:
                return HttpResponse('用户名不能为空')
            id = service.login(None, name, pwd)
            if id != 0:
                request.session['user'] = name
                return HttpResponse('true')
            else:
                return HttpResponse('登录失败，账号或者密码错误')
        img_ = base64.b64decode(img)
        with open("./media/1.jpg", "wb") as fout:
            fout.write(img_)
        img_path = os.path.abspath("./media/1.jpg")
        id = service.login(img_path)
        if id != 0:
            with open('./static/img/' + id + '.jpg', 'wb') as f:
                f.write(img_)
            request.session['user'] = id
            return HttpResponse('true')
        else:
            return HttpResponse('登录失败，您可能不是我们的同学，又或许光线不好')

    def add(self, request):
        return render(request, 'signup.html')

    def add_face(self, request):
        img = request.POST['img']
        stu_no = request.POST['stu_no']
        msg = service.add(img, stu_no)
        if msg == 'OK':
            with open('./static/img/' + stu_no + '.jpg', 'wb') as f:
                f.write(base64.b64decode(img))
        return HttpResponse(msg)
