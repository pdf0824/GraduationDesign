# coding=utf-8

from .Python_sdk.get import get
from ..models import Person


def _doLogin(img, stu_no=None, password=None):
    if img is not None:
        youtu = get()
        result = youtu.FaceIdentify('pdf', img, data_type=0)
        candidates = result['candidates']
        if len(candidates) > 1 and candidates is not None:
            id = candidates[0]['person_id']
            confidence = candidates[0]['confidence']
            if confidence >= 75.0:
                return id
        return 0
    else:
        youtu = get()
        re = youtu.GetInfo(stu_no)['errormsg']
        if re == 'ERROR_PERSON_NOT_EXISTED':
            return 0
        return Person.objects.filter(stu_no=stu_no, password=password).count()
