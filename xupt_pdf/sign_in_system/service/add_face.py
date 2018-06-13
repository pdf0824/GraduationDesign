# coding=utf-8

from .Python_sdk.get import get
from ..models import Person
import base64


def add(img, stu_no):
    exist = Person.objects.all().filter(stu_no=stu_no).exists()
    msg = '没有此用户，注册失败'
    if exist:
        youtu = get()
        result = youtu.AddFace(person_id=stu_no, images=[img], data_type=1)
        msg = str(result.get('errormsg'))
        error_code = str(result.get('errorcode'))
        if error_code == '-1303':
            result = youtu.NewPerson(person_id=stu_no, image_path=img, group_ids=['pdf'], data_type=1)
            msg = str(result.get('errormsg'))
    return msg
