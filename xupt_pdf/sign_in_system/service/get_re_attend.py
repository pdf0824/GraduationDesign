# coding=utf-8
from ..models import ReAttend


def get_re_attend(id):
    return ReAttend.objects.all().filter(stu_no=id)


def get_re_attend_list():
    return ReAttend.objects.all().filter(re_attend_status='1')
