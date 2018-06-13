from picamera.array import PiRGBArray
from picamera import PiCamera
from functools import partial

import multiprocessing as mp
import cv2
import os
import time
import traceback
import sys

sys.path.append("/home/pi/xupt_pdf/sign_in_system/service/Python_sdk")
sys.path.append("/home/pi/xupt_pdf/sign_in_system/service")
sys.path.append("/home/pi/xupt_pdf/sign_in_system")
sys.path.append("/home/pi/xupt_pdf")
from sign_in_system.service.Python_sdk.get import get
import sqlite3
from multiprocessing import Process
import logging
from raspberry_pi.date_utils import *
import shutil
from raspberry_pi.InitDataBase import init_data
from raspberry_pi.count_attend import update
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

led = [38, 40]
GPIO.setup(led, GPIO.OUT)
GPIO.output(led, GPIO.LOW)

take_photos = 37
GPIO.setup(take_photos, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# GPIO.setup(28, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# (0, '迟到'),
# (1, '旷课'),
# (2, '正常'),
# (3, '已补签'),

# 早上一二节打卡开始
one_start = '8:00'
one_end = '10:15'
# 早上三四节打卡开始
two_start = '10:30'
two_end = '12:00'
# 下午一二节打卡开始
three_start = '14:30'
three_end = '16:45'
# 下午七八节打卡开始
four_start = '17:00'
four_end = '19:00'
week_map = {
    1: 'Monday',
    2: 'Tuesday',
    3: 'Wednesday',
    4: 'Thursday',
    5: 'Friday'
}

### Setup #####################################################################  

os.putenv('SDL_FBDEV', '/dev/fb0')

resX = 320
resY = 240

# Setup the camera  
camera = PiCamera()
camera.resolution = (resX, resY)
camera.framerate = 90

t_start = time.time()
fps = 0

# Use this as our output  
rawCapture = PiRGBArray(camera, size=(resX, resY))

# The face cascade file to be used  
face_cascade = cv2.CascadeClassifier('/home/pi/opencv-3.3.0/data/lbpcascades/lbpcascade_frontalface.xml')
out_dir = "./img/"
youtu = get()
i = 0
log = logging.getLogger('raspberry_pi')


def time_cmp(first_time, second_time):
    time1 = first_time.split(':')
    time2 = second_time.split(':')
    if int(time1[0]) > int(time2[0]):
        return 1
    elif int(time1[0]) == int(time2[0]):
        if int(time1[1]) > int(time2[1]):
            return 1
        elif int(time1[1]) == int(time2[1]):
            return 1
        else:
            return -1
    else:
        return -1


def attend(stu_no):
    conn = sqlite3.connect('../db.sqlite3')
    cursor = conn.cursor()
    date = get_date()
    week = get_week()
    re = cursor.execute('SELECT stu_name,class_name FROM T_XUPT_PERSON WHERE stu_no=?', (stu_no,)).fetchone()
    name = re[0]
    class_name = re[1]
    # 获取当天课表
    table = cursor.execute(
        'SELECT ' + week_map[
            week] + ' FROM T_XUPT_TIMETABLE WHERE class_name like "%' + class_name + '%"', ).fetchone()[0]
    time_now = get_time()

    # time_now = '14:30'

    rs = cursor.execute(
        'SELECT attend_one,attend_two,attend_three,attend_four FROM T_XUPT_ATTEND WHERE attend_date=? AND stu_no=?',
        (date, stu_no))
    _time = rs.fetchall()
    print(_time)
    log.info(_time)
    # (0, '迟到'),
    # (1, '旷课'),
    # (2, '正常'),
    # (3, '已补签'),
    try:
        if time_cmp(time_now, '7:00') < 0:
            return False
        if time_cmp(time_now, one_end) < 0:
            if table[0] == '1':
                if len(_time) == 0 or _time[0][0] is None:
                    if time_cmp(time_now, one_start) < 0:
                        cursor.execute(
                            'INSERT INTO T_XUPT_ATTEND '
                            '(stu_no, attend_date, attend_one, stu_name, attend_week, state_one) VALUES (?,?,?,?,?,?)',
                            (stu_no, date, time_now, name, week, 2))
                    else:
                        cursor.execute(
                            'INSERT INTO T_XUPT_ATTEND '
                            '(stu_no, attend_date, attend_one, stu_name, attend_week, state_one) VALUES (?,?,?,?,?,?)',
                            (stu_no, date, time_now, name, week, 0))
                    conn.commit()
                    cursor.close()
                    conn.close()
                    return True
                else:
                    return True
            # one
        if time_cmp(time_now, two_end) < 0 < time_cmp(time_now, '10:00'):
            if table[2] == '1':
                if len(_time) == 0 or _time[0][1] is None:
                    if len(_time) == 0:
                        if time_cmp(time_now, two_start) < 0:
                            cursor.execute(
                                'INSERT INTO T_XUPT_ATTEND '
                                '(stu_no, attend_date, attend_two, stu_name, attend_week, state_two) VALUES (?,?,?,?,?,?)',
                                (stu_no, date, time_now, name, week, 2))
                        # 迟到了
                        else:
                            cursor.execute(
                                'INSERT INTO T_XUPT_ATTEND '
                                '(stu_no, attend_date, attend_two, stu_name, attend_week, state_two) VALUES (?,?,?,?,?,?)',
                                (stu_no, date, time_now, name, week, 0))

                    else:
                        if time_cmp(time_now, two_start) < 0:
                            cursor.execute(
                                'UPDATE T_XUPT_ATTEND SET attend_two=?,state_two=? WHERE attend_date=?',
                                [time_now, 2, date])
                        else:
                            cursor.execute('UPDATE T_XUPT_ATTEND SET attend_two=?,state_two=? WHERE attend_date=?',
                                           [time_now, 0, date])
                    conn.commit()
                    cursor.close()
                    conn.close()
                    return True
                else:
                    return True

            # two
        if time_cmp(time_now, three_end) < 0 < time_cmp(time_now, '13:30'):
            if table[4] == '1':
                if len(_time) == 0 or _time[0][2] is None:
                    if len(_time) == 0:
                        if time_cmp(time_now, three_start) < 0:
                            cursor.execute(
                                'INSERT INTO T_XUPT_ATTEND '
                                '(stu_no, attend_date, attend_three, stu_name, attend_week, state_three) VALUES (?,?,?,?,?,?)',
                                (stu_no, date, time_now, name, week, 2))

                            return True
                        else:
                            cursor.execute(
                                'INSERT INTO T_XUPT_ATTEND '
                                '(stu_no, attend_date, attend_three, stu_name, attend_week, state_three) VALUES (?,?,?,?,?,?)',
                                (stu_no, date, time_now, name, week, 0))
                        conn.commit()
                        cursor.close()
                        conn.close()
                        return True
                    else:
                        if time_cmp(time_now, three_start) < 0:
                            cursor.execute(
                                'UPDATE T_XUPT_ATTEND SET attend_three=?,state_three = ? WHERE attend_date=?',
                                [time_now, 2, date])

                        else:
                            cursor.execute('UPDATE T_XUPT_ATTEND SET attend_three=?, state_three=? WHERE attend_date=?',
                                           [time_now, 0, date])
                        conn.commit()
                        cursor.close()
                        conn.close()
                        return True
                else:
                    return True
            # three
        if time_cmp(time_now, four_end) < 0 < time_cmp(time_now, '16:30'):
            if table[6] == '1':
                if len(_time) == 0 or _time[0][3] is None:
                    if len(_time) == 0:
                        if time_cmp(time_now, four_start) < 0:
                            cursor.execute(
                                'INSERT INTO T_XUPT_ATTEND '
                                '(stu_no, attend_date, attend_four, stu_name, attend_week, state_four) VALUES (?,?,?,?,?,?)',
                                (stu_no, date, time_now, name, week, 2))
                        else:
                            cursor.execute(
                                'INSERT INTO T_XUPT_ATTEND '
                                '(stu_no, attend_date, attend_four, stu_name, attend_week, state_four) VALUES (?,?,?,?,?,?)',
                                (stu_no, date, time_now, name, week, 0))
                        conn.commit()
                        cursor.close()
                        conn.close()
                        return True
                    else:
                        if time_cmp(time_now, four_start) < 0:
                            cursor.execute(
                                'UPDATE T_XUPT_ATTEND SET attend_four=?,state_four=? WHERE attend_date=?',
                                [time_now, 2, date])

                        elif time_cmp(time_now, four_end) < 0:
                            cursor.execute('UPDATE T_XUPT_ATTEND SET attend_four=?,state_four=? WHERE attend_date=?',
                                           [time_now, 0, date])
                        conn.commit()
                        cursor.close()
                        conn.close()
                        return True
                else:
                    return True

            # four
    except:
        print(traceback.print_exc())
    return False


def attend_info(tag=False):
    if tag:
        # 绿灯亮
        GPIO.output(led[0], 1)
        time.sleep(0.3)
        GPIO.output(led[0], 0)
    else:
        GPIO.output(led[1], 1)
        time.sleep(0.3)
        GPIO.output(led[1], 0)


def sign_in(path):
    res = youtu.FaceIdentify('pdf', data_type=0, image_path=path)
    candidates = res.get("candidates")
    if len(candidates) > 1 and candidates is not None:
        id = candidates[0]['person_id']
        confidence = candidates[0]['confidence']
        if confidence >= 75.0:
            try:
                if attend(id):
                    log.info('suc')
                    os.replace(path, out_dir + str(id) + '.jpg')
                    shutil.copy(out_dir + str(id) + '.jpg', '../static/img/')
                    attend_info(True)
                else:
                    log.warning('WARNING:' + id + 'not attend suc')
                    attend_info(False)
            except Exception:
                log.error('ERROR:' + id + 'not attend suc')
                attend_info(False)
    else:
        log.info('请重新拍照')
        attend_info(False)


key = 0
exit_key = 0


def press_key(channel):
    global key
    key = 1


def exit_system(channel):
    global exit_key
    exit_key = 1


GPIO.add_event_detect(take_photos, GPIO.RISING, callback=press_key, bouncetime=200)


# GPIO.add_event_detect(28, GPIO.RISING, callback=exit_system, bouncetime=200)


### Helper Functions ##########################################################

def get_faces(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return face_cascade.detectMultiScale(gray), img


def draw_frame(img, faces):
    global fps
    global time_t
    global key
    global i

    # Draw a rectangle around every face  
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (200, 255, 0), 2)

        # Calculate and show the FPS
    fps = fps + 1
    sfps = fps / (time.time() - t_start)
    cv2.flip(img,0)
    cv2.putText(img, "FPS : " + str(int(sfps)), (10, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    cv2.imshow("Frame", img)
    if key == 1:
        key = 0
        cv2.imwrite(out_dir + str(i) + ".jpg", img)
        sign_in(out_dir + str(i) + ".jpg")
        i += 1

    cv2.waitKey(1)


### Main ######################################################################  

if __name__ == '__main__':
    try:
        p1 = Process(target=init_data)
        p2 = Process(target=update)
        p2.start()
        p1.start()

        pool = mp.Pool(processes=4)

        i = 0
        rList = [None] * 17
        fList = [None] * 17
        iList = [None] * 17

        camera.capture(rawCapture, format="bgr")

        for x in range(17):
            rList[x] = pool.apply_async(get_faces, [rawCapture.array])
            fList[x], iList[x] = rList[x].get()
            fList[x] = []

        rawCapture.truncate(0)

        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            image = frame.array

            if i == 1:
                rList[1] = pool.apply_async(get_faces, [image])
                draw_frame(iList[2], fList[1])

            elif i == 2:
                iList[2] = image
                draw_frame(iList[3], fList[1])

            elif i == 3:
                iList[3] = image
                draw_frame(iList[4], fList[1])

            elif i == 4:
                iList[4] = image
                fList[5], iList[5] = rList[5].get()
                draw_frame(iList[5], fList[5])

            elif i == 5:
                rList[5] = pool.apply_async(get_faces, [image])
                draw_frame(iList[6], fList[5])

            elif i == 6:
                iList[6] = image
                draw_frame(iList[7], fList[5])

            elif i == 7:
                iList[7] = image
                draw_frame(iList[8], fList[5])

            elif i == 8:
                iList[8] = image
                fList[9], iList[9] = rList[9].get()
                draw_frame(iList[9], fList[9])

            elif i == 9:
                rList[9] = pool.apply_async(get_faces, [image])
                draw_frame(iList[10], fList[9])

            elif i == 10:
                iList[10] = image
                draw_frame(iList[11], fList[9])

            elif i == 11:
                iList[11] = image
                draw_frame(iList[12], fList[9])

            elif i == 12:
                iList[12] = image
                fList[13], iList[13] = rList[13].get()
                draw_frame(iList[13], fList[13])

            elif i == 13:
                rList[13] = pool.apply_async(get_faces, [image])
                draw_frame(iList[14], fList[13])

            elif i == 14:
                iList[14] = image
                draw_frame(iList[15], fList[13])

            elif i == 15:
                iList[15] = image
                draw_frame(iList[16], fList[13])

            elif i == 16:
                iList[16] = image
                fList[1], iList[1] = rList[1].get()
                draw_frame(iList[1], fList[1])

                i = 0
            if exit_key == 1:
                sys.exit(0)

            i += 1

            rawCapture.truncate(0)
    except:
        GPIO.clearup()
