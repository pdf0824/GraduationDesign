# coding=utf-8
from ..models import Device


def get_device_name(id):
    return Device.objects.filter(id=id).values('name').get()['name']


def get_device(id):
    return Device.objects.filter(id=id)
