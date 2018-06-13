# coding=utf-8
import random
from ..models import User
import traceback
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
    <title>验证码</title>
</head>
<body>
    <h1>Remote Control System Reset Password</h1>
    <div>
        <p>毕业设计验证码模块</p>
        <p>本次验证码为(验证码一分钟内有效):</p>
        
    
'''
tail = '''
</div>
</body>
</html>
'''


def create():
    num = ''
    for i in range(4):
        num += str(random.randint(0, 9))
    return num


def send_mail(to, num):
    long = con + num + tail
    msg = MIMEText(long, 'html')
    msg["Subject"] = "Remote Control System Change Password Request"
    msg["From"] = "Home:" + user
    msg["To"] = to
    try:
        s = smtplib.SMTP("smtp.163.com", timeout=60)
        s.login(user, pwd)
        s.sendmail(user, to, msg.as_string())
        s.close()
        return 'ok'
    except smtplib.SMTPException:
        print(traceback.print_exc())
        return 'nook'


def check(mail):
    return User.objects.filter(id=mail).exists()


def submit(pwd, id):
    try:
        name = User.objects.filter(id=id).values('user_name')[0]['user_name']
        print(name)
        User.objects.filter(user_name=name).update(pass_word=pwd)
        return 'ok'
    except:
        print(traceback.print_exc())
        return 'nook'
