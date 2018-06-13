# coding=utf-8
from ..models import Attend
from ..models import ReAttend
import traceback


def pass_re_attend(id):
    try:
        ReAttend.objects.filter(id=id).update(re_attend_status=2)
        re_attend = ReAttend.objects.get(id=id)
        attend_status = re_attend.attend_status
        if attend_status == '0':
            Attend.objects.filter(stu_no=re_attend.stu_no, attend_date=re_attend.attend_date) \
                .update(state_one=3)
        elif attend_status == '1':
            Attend.objects.filter(stu_no=re_attend.stu_no, attend_date=re_attend.attend_date) \
                .update(state_two=3)
        elif attend_status == '2':
            Attend.objects.filter(stu_no=re_attend.stu_no, attend_date=re_attend.attend_date) \
                .update(state_three=3)
        else:
            Attend.objects.filter(stu_no=re_attend.stu_no, attend_date=re_attend.attend_date) \
                .update(state_four=3)
        return 'ok'
    except Exception:
        print(traceback.print_exc())
        return 'error'


def not_pass_re_attend(id):
    try:
        ReAttend.objects.filter(id=id).update(re_attend_status=3)
        return 'ok'
    except Exception:
        print(traceback.print_exc())
        return 'error'
