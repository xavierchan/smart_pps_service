# coding: utf-8
# @Time    : 2018/7/12 23:26
# @Author  : xavier

import time
import os
import uuid

from django.template import loader
from common.email_sender import EmailSendUtil
from django.conf import settings
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


def send_email():
    collection = client['waste_email']['configs']
    conf = collection.find_one({'active': True})

    if conf:
        util = EmailSendUtil(host='smtp.163.com', port=25)
        from_addr = 'qwerasdfzxcvxx@163.com'
        from_infos = {
            'addr': from_addr,
            'alias': from_addr.split('@')[0],
            'password': 'CZX764545'
        }
        to_infos = {
            'addr': conf['receiver'],
            'alias': conf['receiver'].split('@')[0]
        }
        for index in xrange(0, int(conf['speed'])):
            content_index = index % 3 if (index % 3) in [1,2,3] else 1
            content = loader.render_to_string('crawler/emails/%s.html' % content_index)
            subject = str(uuid.uuid4()).replace('-', '')
            util.send_email(from_infos, to_infos, email_contents={
                'subject': subject,
                'content': subject + content + subject
            })
            time.sleep(int(conf['sleep']))


if __name__ == '__main__':
    send_email()
