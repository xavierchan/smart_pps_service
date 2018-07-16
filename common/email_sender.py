# coding: utf-8
# @Time    : 2018/7/12 19:03
# @Author  : xavier

import smtplib
import email
import datetime
import os
from django.conf import settings

from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

from pymongo import MongoClient

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smart_pps_service.settings")

MONGODB_SETTINGS = settings.MONGODB
client = MongoClient(
    'mongodb://{user}:{password}@{host}:{port}'.format(user=settings.MONGODB['USER'],
                                                       password=settings.MONGODB['PASSWORD'],
                                                       host=settings.MONGODB['HOST'],
                                                       port=settings.MONGODB['PORT'],
                                                       )
)


class EmailSendUtil(object):
    """docstring for EmailSendUtil"""
    def __init__(self, **kwargs):
        super(EmailSendUtil, self).__init__()
        self.host = kwargs.get('host')
        self.port = kwargs.get('port')

    def _format_addr(self, s):
        name, addr = parseaddr(s)
        return formataddr(
            (
                Header(name, 'utf-8').encode(),
                addr.encode('utf-8') if isinstance(addr, unicode) else addr
            )
        )

    def send_process(self):
        pass
        # 1. 发信箱池

        # 2. IP池

        # 3. 目标邮箱

        # 4. 发送邮件内容池

        # 5. 邮件发送策略

    def send_email(self, from_infos, to_infos, email_contents):
        email_logs = client['waste_email']['logs']

        # msg
        res = ''
        try:
            msg = MIMEMultipart('alternative')
            msg['Message-id'] = email.utils.make_msgid()
            msg['Date'] = email.utils.formatdate()
            msg.attach(MIMEText(email_contents['content'], _subtype='html', _charset='UTF-8'))
            msg['From'] = self._format_addr(u'%s <%s>' % (from_infos['alias'], from_infos['addr']))
            msg['Subject'] = Header(email_contents['subject'], 'utf-8').encode()

            server = smtplib.SMTP(self.host, self.port)
            server.login(from_infos['addr'], from_infos['password'])
            server.sendmail(from_infos['addr'], to_infos['addr'], msg.as_string())
            server.quit()
        except Exception as e:
            res = str(e)

        email_logs.insert({
            'send_time': datetime.datetime.now(),
            'status': 0 if res else 1,
            'sender': from_infos['addr'],
            'receiver': to_infos['addr'],
            'detail': res
        })


if __name__ == '__main__':
    util = EmailSendUtil(host='smtp.163.com', port=25)
    from_infos = {
        'addr': 'xavierchan@163.com',
        'alias': 'xavierchan',
        'password': 'CZX521lsx'
    }
    to_infos = {
        'addr': 'qwerasdfzxcvxx@163.com',
        'alias': 'qwerasdfzxcvxx'
    }
    email_contents = {
        'subject': 'hello',
        'content': 'hello world'
    }
    util.send_email(from_infos, to_infos, email_contents)

