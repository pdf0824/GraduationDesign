# coding=utf-8
from ..models import User


def check_login(id, pwd):
    return User.objects.filter(id=id, pass_word=pwd).exists()
