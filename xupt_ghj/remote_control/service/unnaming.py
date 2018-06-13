# coding=utf-8

from ..models import Device
import traceback


def get_un_naming_count():
    return Device.objects.filter(status=0).count()


def get_un_naming():
    return Device.objects.filter(status=0)


def get_naming():
    return Device.objects.filter(status=1)


def del_device(_id):
    return Device.objects.filter(id=_id).delete()


def change_name(id, name):
    if Device.objects.filter(name=name).exists():
        return "Device name already exits,change other and try again!"
    return Device.objects.filter(id=id).update(name=name, status=1)
