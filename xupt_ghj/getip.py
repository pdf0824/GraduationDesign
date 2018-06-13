# coding=utf-8
import traceback
import subprocess
import smtplib
from email.mime.text import MIMEText

user = 'ghj_baby_baby@163.com'
pwd = 'pdf0824ll'
con = '''
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>ip 信息</title>
</head>
<body>
    


'''
tail = '''
</div>
</body>
</html>
'''

if __name__ == "__main__":
    to = '15114876417@163.com'
    long = subprocess.getoutput('hostname -I')
    print(long)
    long = con + long + tail
    msg = MIMEText(long, 'html')
    msg["Subject"] = "系统 Ip"
    msg["From"] = "Home:" + user
    msg["To"] = '15114876417@163.com'
    try:
        while True:
            try:
                if len(long) != 0:
                    s = smtplib.SMTP("smtp.163.com", timeout=60)
                    s.login(user, pwd)
                    s.sendmail(user, to, msg.as_string())
                    s.close()
                    break
                else:
                    long = subprocess.getoutput('''
                        ifconfig wlan0 | grep "inet addr" | awk '{ print $2}' | awk -F: '{print $2}'
                        ''')
                    print(long)
                    long = con + long + tail
                    msg = MIMEText(long, 'html')
                    msg["Subject"] = "系统 Ip"
                    msg["From"] = "Home:" + user
                    msg["To"] = '15114876417@163.com'
            except:
                continue
    except smtplib.SMTPException:
        print(traceback.print_exc())
