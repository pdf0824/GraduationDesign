# import os
#
# if __name__ == '__main__':
#     os.system('sudo nohup python3 manage.py runserver 0.0.0.0:80 >web.log &')
#     os.system('sudo python3 /home/pi/xupt_pdf/sign_in_system/service/raspberry_pi/main.py')
def time_cmp(first_time, second_time):
    time1 = first_time.split(':')
    time2 = second_time.split(':')
    if int(time1[0]) > int(time2[0]):
        return 1
    elif int(time1[0]) == int(time2[0]):
        if int(time1[1]) > int(time2[1]):
            return 1
        elif int(time1[1]) == int(time2[1]):
            if int(time1[2]) > int(time2[2]):
                return 1
            else:
                return -1
        else:
            return -1
    else:
        return -1


print(time_cmp('13:30', '11:06'))
