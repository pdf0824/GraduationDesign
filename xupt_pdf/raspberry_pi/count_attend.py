# coding=utf-8
import schedule as sc
import sqlite3
import datetime

# 早上一二节打卡开始、结束
one_start = '8:00'
one_end = '10:15'
# 早上三四节打卡开始、结束
two_start = '10:30'
two_end = '12:00'
# 下午一二节打卡开始、结束
three_start = '14:30'
three_end = '16:45'
# 下午七八节打卡开始、结束
four_start = '17:00'
four_end = '19:00'


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


week = datetime.datetime.now().isoweekday()
date = datetime.date.today()

week_map = {
    1: 'Monday',
    2: 'Tuesday',
    3: 'Wednesday',
    4: 'Thursday',
    5: 'Friday',
}


def count_one():
    conn = sqlite3.connect('../db.sqlite3')
    cursor = conn.cursor()
    # cursor.execute('INSERT INTO main.T_XUPT_ATTEND (stu_no,attend_date,attend_one) VALUES (?,?,?)', ['06141112', date,'10:11'])
    _class_name = ["".join(_class)[0:-2] for _class in
                   cursor.execute(
                       'SELECT class_name FROM T_XUPT_TIMETABLE WHERE ' + week_map[week] + ' like "11%"').fetchall()]
    for class_name in _class_name:
        _stu_no = ["".join(_id) for _id in
                   cursor.execute('SELECT stu_no FROM T_XUPT_PERSON WHERE class_name=? '
                                  'AND stu_no NOT IN '
                                  '(SELECT stu_no FROM T_XUPT_ATTEND WHERE attend_date=? AND attend_one  NOTNULL )',
                                  [class_name, date]).fetchall()]
        # print(_stu_no)
        for stu_no in _stu_no:
            try:
                re = cursor.execute(
                    'UPDATE T_XUPT_ATTEND SET state_one=1 WHERE attend_date=? AND stu_no=?', [date, stu_no]
                ).fetchone()
                if re is None:
                    cursor.execute(
                        'INSERT INTO T_XUPT_ATTEND (state_one,attend_date,stu_no) VALUES (1,?,?)', [date, stu_no]
                    )
            except:
                print('error in update')
    print('suc')
    conn.commit()
    cursor.close()
    conn.close()


def count_two():
    conn = sqlite3.connect('../db.sqlite3')
    cursor = conn.cursor()
    # cursor.execute('INSERT INTO main.T_XUPT_ATTEND (stu_no,attend_date,attend_one) VALUES (?,?,?)', ['06141112', date,'10:11'])
    _class_name = ["".join(_class)[0:-2] for _class in
                   cursor.execute(
                       'SELECT class_name FROM T_XUPT_TIMETABLE WHERE ' + week_map[week] + ' like "??11%"').fetchall()]
    for class_name in _class_name:
        _stu_no = ["".join(_id) for _id in
                   cursor.execute('SELECT stu_no FROM T_XUPT_PERSON WHERE class_name=? '
                                  'AND stu_no NOT IN '
                                  '(SELECT stu_no FROM T_XUPT_ATTEND WHERE attend_date=? AND attend_two  NOTNULL )',
                                  [class_name, date]).fetchall()]
        # print(_stu_no)
        for stu_no in _stu_no:
            try:
                re = cursor.execute(
                    'UPDATE T_XUPT_ATTEND SET state_two=1 WHERE attend_date=? AND stu_no=?', [date, stu_no]
                ).fetchone()
                if re is None:
                    cursor.execute(
                        'INSERT INTO T_XUPT_ATTEND (state_two,attend_date,stu_no) VALUES (1,?,?)', [date, stu_no]
                    )
            except:
                print('error in update')
    print('suc')
    conn.commit()
    cursor.close()
    conn.close()


def count_three():
    conn = sqlite3.connect('../db.sqlite3')
    cursor = conn.cursor()
    # cursor.execute('INSERT INTO main.T_XUPT_ATTEND (stu_no,attend_date,attend_one) VALUES (?,?,?)', ['06141112', date,'10:11'])
    _class_name = ["".join(_class)[0:-2] for _class in
                   cursor.execute(
                       'SELECT class_name FROM T_XUPT_TIMETABLE WHERE ' + week_map[
                           week] + ' like "????11%"').fetchall()]
    for class_name in _class_name:
        _stu_no = ["".join(_id) for _id in
                   cursor.execute('SELECT stu_no FROM T_XUPT_PERSON WHERE class_name=? '
                                  'AND stu_no NOT IN '
                                  '(SELECT stu_no FROM T_XUPT_ATTEND WHERE attend_date=? AND attend_three  NOTNULL )',
                                  [class_name, date]).fetchall()]
        # print(_stu_no)
        for stu_no in _stu_no:
            try:
                re = cursor.execute(
                    'UPDATE T_XUPT_ATTEND SET state_three=1 WHERE attend_date=? AND stu_no=?', [date, stu_no]
                ).fetchone()
                if re is None:
                    cursor.execute(
                        'INSERT INTO T_XUPT_ATTEND (state_three,attend_date,stu_no) VALUES (1,?,?)', [date, stu_no]
                    )
            except:
                print('error in update')
    print('suc')
    conn.commit()
    cursor.close()
    conn.close()


def count_four():
    conn = sqlite3.connect('../db.sqlite3')
    cursor = conn.cursor()
    # cursor.execute('INSERT INTO main.T_XUPT_ATTEND (stu_no,attend_date,attend_one) VALUES (?,?,?)', ['06141112', date,'10:11'])
    _class_name = ["".join(_class)[0:-2] for _class in
                   cursor.execute(
                       'SELECT class_name FROM T_XUPT_TIMETABLE WHERE ' + week_map[
                           week] + ' like "??????11"').fetchall()]
    for class_name in _class_name:
        _stu_no = ["".join(_id) for _id in
                   cursor.execute('SELECT stu_no FROM T_XUPT_PERSON WHERE class_name=? '
                                  'AND stu_no NOT IN '
                                  '(SELECT stu_no FROM T_XUPT_ATTEND WHERE attend_date=? AND attend_four  NOTNULL )',
                                  [class_name, date]).fetchall()]
        # print(_stu_no)
        for stu_no in _stu_no:
            try:
                re = cursor.execute(
                    'UPDATE T_XUPT_ATTEND SET state_four=1 WHERE attend_date=? AND stu_no=?', [date, stu_no]
                ).fetchone()
                if re is None:
                    cursor.execute(
                        'INSERT INTO T_XUPT_ATTEND (state_four,attend_date,stu_no) VALUES (1,?,?)', [date, stu_no]
                    )
            except:
                print('error in update')
    print('suc')
    conn.commit()
    cursor.close()
    conn.close()


sc.every().day.at(one_end).do(count_one)
sc.every().day.at(two_end).do(count_two)
sc.every().day.at(three_end).do(count_three)
sc.every().day.at(four_end).do(count_four)


def update():
    while True:
        if week == 6 or week == 7:
            continue
        sc.run_pending()
