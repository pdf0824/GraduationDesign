import sys
import codecs
import os
import RPi.GPIO as GPIO
import time
from pad4pi import rpi_gpio
import pexpect
import uuid
import traceback
import sqlite3
import datetime
import subprocess

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# ******************************************#


key_map = {
    'KEY_0': 'key_zero',
    'KEY_1': 'key_one',
    'KEY_2': 'key_two',
    'KEY_3': 'key_three',
    'KEY_4': 'key_four',
    'KEY_5': 'key_five',
    'KEY_6': 'key_six',
    'KEY_7': 'key_seven',
    'KEY_8': 'key_eight',
    'KEY_9': 'key_nine',
    'KEY_VOLUMEUP': 'key_volume_up',
    'KEY_VOLUMEDOWN': 'key_volume_down',
    'KEY_CHANNELUP': 'key_channel_up',
    'KEY_CHANNELDOWN': 'key_channel_down',
}


def printKey(key):
    # print(key)
    global study
    global study_key
    global press_key
    if key == 'study':
        '''print(key)'''
        study = not study
        # return
    if key != 'None':
        press_key = key
        study_key.append(key)
        GPIO.output(OUT_PINS[1], GPIO.LOW)
        GPIO.output(OUT_PINS[2], GPIO.LOW)


KEYPAD1 = [
    ["KEY_VOLUMEUP", "KEY_UP", "KEY_CHANNELUP", "None"],
    ["KEY_LEFT", "KEY_OK", "KEY_RIGHT", "None"],
    ["KEY_VOLUMEDOWN", "KEY_DOWN", "KEY_CHANNELDOWN", "None"],
    ["None", "None", "None", "KEY_MODE"]
]
KEYPAD2 = [
    ['KEY_0', 'KEY_1', 'KEY_2', 'KEY_3'],
    ['KEY_4', 'KEY_5', 'KEY_6', 'KEY_7'],
    ['KEY_8', 'KEY_9', 'None', 'None'],
    ['KEY_POWER', 'KEY_HOME', 'KEY_BACK', 'study']
]
COL_PINS1 = [2, 3, 4, 10]  # BCM numbering
ROW_PINS1 = [24, 23, 15, 14]  # BCM numbering
COL_PINS2 = [9, 11, 5, 6]  # BCM numbering
ROW_PINS2 = [12, 7, 8, 25]  # BCM numbering
factory1 = rpi_gpio.KeypadFactory()
factory2 = rpi_gpio.KeypadFactory()
keypad1 = factory1.create_keypad(keypad=KEYPAD1, row_pins=ROW_PINS1, col_pins=COL_PINS1, key_delay=200)
keypad2 = factory2.create_keypad(keypad=KEYPAD2, row_pins=ROW_PINS2, col_pins=COL_PINS2, key_delay=200)
keypad1.registerKeyPressHandler(prin    tKey)
keypad2.registerKeyPressHandler(printKey)
'''
1 13 16 19 20 21 26 
'''
OUT_PINS = [20, 13, 16, 19, 1, 21, 26]
GPIO.setup(OUT_PINS, GPIO.OUT)
GPIO.output(OUT_PINS, GPIO.LOW)
study = False
press_key = None
li = [
    'Press RETURN to continue.',
    'Press RETURN now to start recording.',
    'irrecord: no data for 10 secs, aborting',
    'Please enter the name for the next button (press <ENTER> to finish recording)',
    'The last button did not seem to generate any signal.\nPress RETURN to continue.',
    pexpect.EOF,
    pexpect.TIMEOUT
]

# ******************************************#
study_key = []
remote_name = None


def update(file_str, remote):
    exits_key = []
    param = []
    param.append(remote)
    param.append(os.path.abspath(remote))
    param.append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    param.append(0)
    value = '(?,?,?,?,'
    sql = 'insert into T_XUPT_DEVICE (remote, path,create_time,status,'
    for i in study_key:
        if i in file_str:
            if i in exits_key:
                continue
            exits_key.append(i)
            try:
                sql += key_map[i] + ','
            except:
                sql += i + ','
            param.append(1)
            value += '?,'
    if len(param) == 4:
        return False
    sql = sql[0:-1] + ')'
    value = value[0:-1] + ')'
    sql = sql + 'values' + value
    exits_key = []
    conn = sqlite3.connect('../db.sqlite3')
    cursor = conn.cursor()
    try:
        cursor.execute(sql, param)
        conn.commit()
        return True
    except:
        print(traceback.print_exc())
    print(sql)
    return False


# ******************************************#

# printKey will be called each time a keypad button is pressed

if __name__ == '__main__':

    try:
        while True:
            if study:
                remote_name = None
                # 保存当前设备的名字（当前设备的名字初始化为none）
                GPIO.output(OUT_PINS[0], GPIO.HIGH)
                # 进入学习状态使A灯变亮
                os.system('sudo /etc/init.d/lirc stop')
                # 录制之前关闭Lirc
                name = str(uuid.uuid1())
                # 先获取一个uuid字符串
                p = pexpect.spawnu('sudo irrecord -f -d /dev/lirc0 ' + name, logfile=sys.stdout)
                # 执行这条录制命令
                while True:
                    # 循环匹配，因为录制命令是持续的状态
                    index = p.expect_exact(li, timeout=200)
                    # 匹配li中可能结果返回对应的索引
                    if index == 0 or index == 1:
                        p.sendline()
                    #     如果索引是0或者1的时候给lirc发送回车
                    elif index == 2:
                        pass
                    #      如果索引是2的时候不做任何操作
                    elif index == 3:
                        # 如果索引为3，lirc提示接收按键值，让B灯亮
                        GPIO.output(OUT_PINS[1], GPIO.HIGH)
                        try:
                            while GPIO.input(OUT_PINS[1]):
                                # 只要B灯一直亮着（对应的引脚一直是高电平），则循环判断全局变量study的状态
                                if not study:
                                    # 如果按下study 给lirc发送回车，退出学习
                                    p.sendline()
                                    GPIO.output(OUT_PINS[1], GPIO.LOW)
                                    GPIO.output(OUT_PINS[2], GPIO.LOW)
                                    # 让BC灯接的引脚变为低电平
                                    continue
                        except Exception:
                            # 程序出现异常退出匹配
                            print("exception")
                            break
                        p.sendline(press_key)
                    #     发送当前按键值
                    elif index == 4:
                        # 发送了按键值，但是没有接到红外信号，C灯亮
                        GPIO.output(OUT_PINS[2], GPIO.HIGH)
                    elif index == 5:
                        # 索引为5，录制命令结束
                        if os.path.exists(name):
                            # 判断是否生成该设备，没有生成则直接退出，学习成功则
                            # 将学习完成的一些信息持久化到sqlite3数据库中
                            device = codecs.open(name).read().decode()
                            # 获取当前设备中的内容
                            iscp = update(device, name)
                            # 调用持久化函数，参数为设备内容以及设备名字
                            if iscp:
                                # 如果存到数据库成功的话，将设备复制到/etc/lirc/lircd.conf
                                # 重启lirc
                                os.system('sudo cp ' + name + ' /etc/lirc/lircd.conf')
                                os.system('sudo /etc/init.d/lirc start')
                                remote_name = name
                        #         保存当前设备的名字
                        break
                    elif index == 6:
                        # 如果无法匹配到结果，并超时，则重新继续等待匹配
                        pass
                # 学习结束，A灯灭，全局变量study取False
                print('end')
                study = False
                GPIO.output(OUT_PINS[0], GPIO.LOW)
            else:
                if press_key is not None:
                    # 如果当前按键值不是None才执行，是None说明按键没有用
                    if remote_name is None:
                        # 如果当前设备名字是None（即不知道当前设备的名字）
                        result = subprocess.getoutput('sudo irsend list "" ""')
                        # 获取设备名字
                        if 'refused' in result:
                            # 重启lirc
                            os.system('sudo /etc/init.d/lirc restart')
                            os.system('sudo lircd start')
                            os.system('sudo lircd -d /dev/lirc0')
                            result = subprocess.getoutput('sudo irsend list "" ""')
                        #     再次获取获取设备名字
                        if len(result) != 0:
                            remote_name = result.split(':')[1]
                    #         如果设备名字返回成功则保存当前设备名字
                    result = subprocess.getoutput('sudo irsend SEND_ONCE ' + remote_name + ' ' + press_key)
                    # 发送红外
                    if len(result) == 0:
                        # 发送成功没有返回信息，所以长度为0，D灯闪一下
                        GPIO.output(OUT_PINS[3], GPIO.HIGH)
                        time.sleep(0.3)
                        GPIO.output(OUT_PINS[3], GPIO.LOW)
                        print(press_key, 'suc')
                    else:
                        # 长度不为0说明红外发送失败
                        print(press_key, 'error')
                    press_key = None
    except:
        # 运行报错退出，恢复原GPIO状态
        print(traceback.print_exc())
        GPIO.cleanup()
    GPIO.cleanup()
