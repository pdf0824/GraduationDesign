# coding=utf-8
from ..models import ReAttend


def get_msg_count():
    return ReAttend.objects.all().filter(re_attend_status='1').count()
