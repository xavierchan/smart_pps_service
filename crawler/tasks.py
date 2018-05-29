# coding: utf-8
# @Time    : 2018/5/28 16:22
# @Author  : xavier
from __future__ import absolute_import, unicode_literals

import requests

from bs4 import BeautifulSoup
from smart_pps_service.celery import app
from celery import shared_task


@shared_task
def hello():
    return 'hello world'


@shared_task
def crawl_lagou(url):
    print('正在抓取链接{}'.format(url))
    resp_text = requests.get(url).text
    soup = BeautifulSoup(resp_text, 'html.parser')
    return soup.find('h1').text
