# coding=utf-8
from ..models import Person

from ..models import Attend


def get_user(id):
    print('get_user_info', id)
    li = Person.objects.get(stu_no=id)
    return li


def get_attend(id, date):
    li = Attend.objects.all().filter(stu_no=id, attend_date__lte=date)
    return li
