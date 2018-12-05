# coding: utf-8
# @Time    : 2018/7/25 00:13
# @Author  : xavier

# coding: utf-8

import socks
import smtplib
import traceback
import email
import random
import uuid
import time
from django.db.models import Q
from xsmtplib import SMTP

from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


mails = [
    'qwerasdfzxcvxxx@sohu.com',
    'qwerasdfzxcvccc@sohu.com',
    'qwerasdfzxcvxx@163.com',
    'qwerasdfzxcvccc@163.com',
    # 'sohuqazwsxedcrfv@sohu.com',
    'qazwsxedcrfvczx@163.com',
    'sohuplmoknijbuhv@sohu.com',
]


smtps = {
    'sohu': 'smtp.sohu.com',
    '163': 'smtp.163.com'
}


def random_num(num):
    '''
    随机数字
    :param num: 
    :return: 
    '''
    data = list('0123456789')
    return ''.join(random.sample(data, num))


def random_zm(num):
    '''
    随机字母
    :param num: 
    :return: 
    '''
    data = list('qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM')
    return ''.join(random.sample(data, num))


def random_pinyin(num):
    '''
    随机中文
    :param num: 
    :return: 
    '''
    return ''.join(
        [unichr(random.randint(0x4e00, 0x9fa5)) for x in xrange(0, num)]
    )


def create_uuid(num):
    '''
    生成uuid
    :return: 
    '''
    return str(uuid.uuid4())


def random_sysdn(num):
    '''
    随机符号
    '''
    data = list(' ~`!@#$%^&*()-=_+|;:",.<>')
    return ''.join(random.sample(data, num))


random_func = [
    random_num,
    random_zm,
    random_pinyin,
    create_uuid,
    random_sysdn
]


def random_subject():
    '''
    随机主题
    '''
    nums = random_num(5)
    subject_list = [random_func[nums.index(item)](int(item)) for item in nums]
    subject = ''.join(subject_list)
    return subject


def random_content():
    '''
    随机内容
    '''
    content = ''.join([random_subject() for item in xrange(0, 30)])
    return content


def send_email(addr, pwd):
    try:
        target = '407084254@qq.com'

        msg = MIMEMultipart('alternative')
        msg['Message-id'] = email.utils.make_msgid()
        msg['Date'] = email.utils.formatdate()
        msg['From'] = addr
        msg['To'] = target
        msg['Subject'] = Header(random_subject(), 'utf-8').encode()
        msg.attach(
            MIMEText(
                random_content(),
                _subtype='html',
                _charset='UTF-8'
            )
        )

        backend = addr.split('@')[1].split('.')[0]
        server = smtplib.SMTP(smtps[backend], 25)
        # server = SMTP(host=smtps[backend], port=25, proxy_host='182.91.122.122', proxy_port=9999)
        server.login(addr, pwd)
        server.sendmail(addr, target, msg.as_string())
        server.quit()
    except Exception as e:
        traceback.print_exc()
        print str(e)


if __name__ == '__main__':
    n = 0
    # socks.set_default_proxy(socks.PROXY_TYPE_SOCKS5, '182.91.122.122', 9999)
    # socks.wrap_module(smtplib)
    while n < 180:
        index = n % len(mails)
        send_email(mails[index], 'CZX764545')
        n += 1
        print 'send ' + str(n) + mails[index]
        time.sleep(1)

