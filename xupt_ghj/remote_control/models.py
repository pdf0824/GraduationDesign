from django.db import models


# Create your models here.

class User(models.Model):
    user_name = models.CharField('姓名', max_length=255, null=True)
    pass_word = models.CharField('密码', max_length=255)
    id = models.CharField('账号', max_length=255, primary_key=id)

    class Meta:
        db_table = 'T_XUPT_USER'


class Device(models.Model):
    name = models.CharField('自定义设备名字', max_length=255, unique=True, null=True)
    remote = models.CharField('自动生成设备名字', max_length=255, unique=True)
    path = models.CharField('设备路径', max_length=255, unique=True)
    status = models.IntegerField('是否已完成命名，0没有，1完成', null=True)
    create_time = models.CharField('设备创建时间', max_length=255, null=True)
    key_power = models.CharField('开关键', max_length=255, null=True)
    key_one = models.CharField('1键', max_length=255, null=True)
    key_two = models.CharField('2键', max_length=255, null=True)
    key_three = models.CharField('3键', max_length=255, null=True)
    key_four = models.CharField('4键', max_length=255, null=True)
    key_five = models.CharField('5键', max_length=255, null=True)
    key_six = models.CharField('6键', max_length=255, null=True)
    key_seven = models.CharField('7键', max_length=255, null=True)
    key_eight = models.CharField('8键', max_length=255, null=True)
    key_nine = models.CharField('9键', max_length=255, null=True)
    key_zero = models.CharField('0键', max_length=255, null=True)
    key_up = models.CharField('上键', max_length=255, null=True)
    key_down = models.CharField('下键', max_length=255, null=True)
    key_left = models.CharField('左键', max_length=255, null=True)
    key_right = models.CharField('右键', max_length=255, null=True)
    key_ok = models.CharField('ok键', max_length=255, null=True)
    key_back = models.CharField('返回键', max_length=255, null=True)
    key_home = models.CharField('主页键', max_length=255, null=True)
    key_mode = models.CharField('空调键', max_length=255, null=True)
    key_volume_up = models.CharField('音量加键', max_length=255, null=True)
    key_volume_down = models.CharField('音量减键', max_length=255, null=True)
    key_channel_up = models.CharField('频道加键', max_length=255, null=True)
    key_channel_down = models.CharField('频道减键', max_length=255, null=True)

    class Meta:
        db_table = 'T_XUPT_DEVICE'
