# coding=utf-8

import time
import datetime
import os

#
# print(os.path.abspath('../../db.sqlite3'))
#
# li = list(dict())
# li.append({})
# print(len(li))
# print(time)
# print(time.time())
# print(time.clock())
# print(datetime)
# print(datetime.date)
# print(datetime.time)
# print(time.strftime('%Y-%m-%d', time.localtime(time.time())))
# print(time.strftime('%H:%M:%S', time.localtime(time.time())))
# print(datetime.datetime.now().isoweekday())
# p
print(time.time())
a = time.time()
time.sleep(1)
if time.time() - a > 1:
    print(time.time())
