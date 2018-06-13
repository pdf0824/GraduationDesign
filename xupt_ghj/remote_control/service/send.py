# coding=utf-8
from ..models import Device
import os
import traceback
import subprocess
import redis


def send(device, key):
    try:
        device = Device.objects.filter(name=device).values('path', 'remote')
        result = subprocess.getoutput('sudo cp ' + device.get()['path'] + ' /etc/lirc/lircd.conf')
        if len(result) != 0:
            return False
        send_com = 'sudo irsend SEND_ONCE ' + device.get()['remote'] + ' ' + key
        result = subprocess.getoutput(send_com)
        if 'Connection refused' in result:
            os.system('sudo /etc/init.d/lirc restart')
            os.system('sudo lircd start')
            os.system('sudo lircd -d /dev/lirc0')
            result = subprocess.getoutput(send_com)
        if len(result) == 0:
            return True
        else:
            return False
    except:
        print(traceback.print_exc())
        return False
