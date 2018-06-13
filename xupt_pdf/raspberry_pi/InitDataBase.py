# coding=utf-8
import xlrd
import random
import sqlite3
from datetime import datetime

conn = sqlite3.connect('../db.sqlite3')
# 创建一个cursor
cursor = conn.cursor()


def init_data():
    excel = xlrd.open_workbook(r'./person.xls')
    sheet0 = excel.sheet_by_index(0)
    user_rows = sheet0.nrows - 3
    for i in range(user_rows):
        li = list()
        row = sheet0.row_values(i + 3)
        li.append(i)  # id
        li.append(row[0])
        li.append(str(row[1]))
        li.append(row[2])
        li.append(row[3])
        li.append(row[4])
        li.append(row[5])
        li.append(row[6])
        li.append(int(row[7]))
        li.append(row[8])
        d = datetime(*xlrd.xldate_as_tuple(row[9], 0))
        li.append(d)
        try:
            cursor.execute('INSERT INTO '
                           'T_XUPT_PERSON '
                           'VALUES (?,?,?,?,?,?,?,?,?,?,?)', li)
        except:
            pass
    sheet1 = excel.sheet_by_index(1)
    rows = sheet1.nrows
    Mon = ''
    Tues = ''
    Wed = ''
    Thur = ''
    Fri = ''
    class_name = ''
    for i in range(rows):
        row = sheet1.row_values(i)
        if i % 9 == 0:
            class_name = row[0]
            continue
        Mon += str(int(row[2]))
        Tues += str(int(row[3]))
        Wed += str(int(row[4]))
        Thur += str(int(row[5]))
        Fri += str(int(row[6]))

        if (i + 1) % 9 == 0 and (i + 1) / 9 != 0:
            try:
                cursor.execute(
                    'INSERT INTO T_XUPT_TIMETABLE(class_name, Monday, Tuesday, '
                    'Wednesday, Thursday, Friday) VALUES (?,?,?,?,?,?)', [class_name, Mon, Tues, Wed, Thur, Fri])
            except:
                cursor.execute('UPDATE T_XUPT_TIMETABLE SET Monday=?,Tuesday=?,Wednesday=?,Thursday=?,'
                               'Friday=?', [Mon, Tues, Wed, Thur, Fri])
            class_name = Mon = Tues = Wed = Thur = Fri = ''

    conn.commit()
    cursor.close()
    conn.close()
