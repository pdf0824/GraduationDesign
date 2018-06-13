# coding=utf-8
from wxpy import *
import os
import subprocess
import redis
import sqlite3
import traceback

qr_path = 'C:/Users/ghj/Desktop/xupt_ghj/static/wx/wx.png'
# qr_path = './wx.png'
msg_head = 'root:\n{\n'
msg_tail = '\n}\nroot-end'
remote = None
key = None
name = None
path = None
key_value = {
    'key_one': '1键',
    'key_two': '2键',
    'key_three': '3键',
    'key_four': '4键',
    'key_five': '5键',
    'key_six': '6键',
    'key_seven': '7键',
    'key_eight': '8键',
    'key_nine': '9键',
    'key_zero': '0键',
    'key_ok': 'OK键',
    'key_back': '返回键',
    'key_home': '主页键',
    'key_up': '上键',
    'key_down': '下键',
    'key_left': '左键',
    'key_right': '右键',
    'key_volume_up': '音量加键',
    'key_volume_down': '音量减键',
    'key_channel_up': '频道加键',
    'key_channel_down': '频道减键',
    'key_power': '开关键',
    'key_mode': '空调键',
}
value_key = {
    '1键': 'KEY_1',
}
r = redis.Redis(host='localhost', port=6379, decode_responses=True)
user = None


def login_callback():
    global user
    r.set(user, True)
    if os.path.exists(qr_path):
        os.remove(qr_path)


def logout_callback():
    global user
    r.delete(user)
    r.delete('key_str')
    if os.path.exists(qr_path):
        os.remove(qr_path)
    os.system('kill ' + str(os.getpid()))


conn = sqlite3.connect('../db.sqlite3', check_same_thread=False)
cursor = conn.cursor()
# user = sys.argv[1]
user = 'ghj'
bot = Bot(qr_path=qr_path, login_callback=login_callback, logout_callback=logout_callback, cache_path=True,console_qr=False)
robot = Tuling(api_key='4c533f458985456c87991a9066d924d5')
try:
    bot.self.send('Login Success!')
except:
    print('in')
    bot.self.add()
    bot.self.accept()
    bot.self.send('Login Success!')


# my_friend = bot.friends().search('nsd', sex=MALE)[0]

# bot.file_helper.send('hello world!')

@bot.register(bot.self, except_self=False)
def reply_self(msg):
    global remote, path, name, key
    if '退出' in msg.text:
        bot.self.send(msg_head + '已退出' + msg_tail)
        bot.logout()
    elif '查看设备' in msg.text:
        try:
            re = cursor.execute('SELECT name FROM T_XUPT_DEVICE WHERE status=1').fetchall()
            print(re)
            i = 0
            device_str = ''
            for device in re:
                device_str += str(i) + '、' + device[0] + '\n'
                i += 1
            device_str += '请回复：使用+设备名'
            bot.self.send(device_str)
        except:
            bot.self.send(traceback.print_exc())
        return
    elif '使用' == msg.text[0:2]:
        try:
            if name == msg.text[2:]:
                bot.self.send(r.get('key_str'))
                return
            name = msg.text[2:]
            re = cursor.execute(
                'SELECT remote,path,key_power,key_one,key_two,key_three,key_four,key_five,'
                'key_six,key_seven,key_eight,key_nine,key_zero,key_ok,key_left,key_right,key_up,key_down,'
                'key_channel_down,key_channel_up,key_volume_down,key_volume_up,key_mode,key_home,key_back '
                'FROM T_XUPT_DEVICE WHERE name=?', [name, ]).fetchone()
            path = re[1]
            remote = re[0]
            return_str = '设备"' + name + '"的按键有:\n'
            i = 1
            if re[2] is not None and len(re[2]) == 1:
                return_str += str(i) + '、' + key_value['key_power'] + '\n'
                i += 1
            if re[3] is not None and len(re[3]) == 1:
                return_str += str(i) + '、' + key_value['key_one'] + '\n'
                i += 1
            if re[4] is not None and len(re[4]) == 1:
                return_str += str(i) + '、' + key_value['key_two'] + '\n'
                i += 1
            if re[5] is not None and len(re[5]) == 1:
                return_str += str(i) + '、' + key_value['key_three'] + '\n'
                i += 1
            if re[6] is not None and len(re[6]) == 1:
                return_str += str(i) + '、' + key_value['key_four'] + '\n'
                i += 1
            if re[7] is not None and len(re[7]) == 1:
                return_str += str(i) + '、' + key_value['key_five'] + '\n'
                i += 1
            if re[8] is not None and len(re[8]) == 1:
                return_str += str(i) + '、' + key_value['key_six'] + '\n'
                i += 1
            if re[9] is not None and len(re[9]) == 1:
                return_str += str(i) + '、' + key_value['key_seven'] + '\n'
                i += 1
            if re[10] is not None and len(re[10]) == 1:
                return_str += str(i) + '、' + key_value['key_eight'] + '\n'
                i += 1
            if re[11] is not None and len(re[11]) == 1:
                return_str += str(i) + '、' + key_value['key_nine'] + '\n'
                i += 1
            if re[12] is not None and len(re[12]) == 1:
                return_str += str(i) + '、' + key_value['key_zero'] + '\n'
                i += 1
            if re[13] is not None and len(re[13]) == 1:
                return_str += str(i) + '、' + key_value['key_ok'] + '\n'
                i += 1
            if re[14] is not None and len(re[14]) == 1:
                return_str += str(i) + '、' + key_value['key_left'] + '\n'
                i += 1
            if re[15] is not None and len(re[15]) == 1:
                return_str += str(i) + '、' + key_value['key_right'] + '\n'
                i += 1
            if re[16] is not None and len(re[16]) == 1:
                return_str += str(i) + '、' + key_value['key_up'] + '\n'
                i += 1
            if re[17] is not None and len(re[17]) == 1:
                return_str += str(i) + '、' + key_value['key_down'] + '\n'
                i += 1
            if re[18] is not None and len(re[18]) == 1:
                return_str += str(i) + '、' + key_value['key_channel_down'] + '\n'
                i += 1
            if re[19] is not None and len(re[19]) == 1:
                return_str += str(i) + '、' + key_value['key_channel_up'] + '\n'
                i += 1
            if re[20] is not None and len(re[20]) == 1:
                return_str += str(i) + '、' + key_value['key_volume_down'] + '\n'
                i += 1
            if re[21] is not None and len(re[21]) == 1:
                return_str += str(i) + '、' + key_value['key_volume_up'] + '\n'
                i += 1
            if re[22] is not None and len(re[22]) == 1:
                return_str += str(i) + '、' + key_value['key_mode'] + '\n'
                i += 1
            if re[23] is not None and len(re[23]) == 1:
                return_str += str(i) + '、' + key_value['key_home'] + '\n'
                i += 1
            if re[24] is not None and len(re[24]) == 1:
                return_str += str(i) + '、' + key_value['key_back'] + '\n'
                i += 1
            return_str += '共' + str(i - 1) + '个，请回复：按下+按键名\n'
            r.set('key_str', return_str)
            bot.self.send(return_str)
        except:
            bot.self.send('错误,请检查参数')
        return
    elif '按下' == msg.text[0:2]:
        key_name = msg.text[2:]
        if key_name not in r.get('key_str'):
            bot.self.send('请检查，没有此按键')
            return
        key = value_key[key_name]
        try:
            result = subprocess.getoutput('sudo cp ' + path + ' /etc/lirc/lircd.conf')
            if len(result) != 0:
                return False
            send_com = 'sudo irsend SEND_ONCE ' + remote + ' ' + key
            result = subprocess.getoutput(send_com)
            if 'Connection refused' in result:
                os.system('sudo /etc/init.d/lirc restart')
                os.system('sudo lircd start')
                os.system('sudo lircd -d /dev/lirc0')
                result = subprocess.getoutput(send_com)
            if len(result) == 0:
                bot.self.send('已发送指令')
            else:
                bot.self.send('错误发生，请查看log')
        except:
            bot.self.send('错误发生，请查看log')
        return
    robot.do_reply(msg)


embed()
