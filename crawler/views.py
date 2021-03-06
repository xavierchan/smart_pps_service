# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import urllib2
import json
from urllib import urlencode

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.shortcuts import render
from django.http.response import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from pymongo import MongoClient
import pymongo
from bs4 import BeautifulSoup

from common.email_sender import EmailSendUtil
from utils import get_as_cp
from smart_pps_service.common.common import xresult, to_int

MONGODB_SETTINGS = settings.MONGODB
client = MongoClient(
    'mongodb://{user}:{password}@{host}:{port}'.format(user=settings.MONGODB['USER'],
                                                       password=settings.MONGODB['PASSWORD'],
                                                       host=settings.MONGODB['HOST'],
                                                       port=settings.MONGODB['PORT'],
                                                       )
)


@login_required
def index(request):
    return render(request, 'crawler/index.html')


def toutiao(request):
    from selenium import webdriver
    import os
    chrome_driver_path = os.path.abspath('') + '/crawler/driver/chromedriver'

    browser = webdriver.Chrome(executable_path=chrome_driver_path)
    browser.get('https://www.toutiao.com/ch/news_tech/')
    user_id = browser.get_cookie('tt_webid').get('value')
    as_cp = browser.execute_script('return ascp.getHoney()')
    _signature = browser.execute_script('return TAC.sign("%s")' % user_id)
    categorys = [
        'new_hot', 'new_game'
    ]

    # as_cp = get_as_cp()
    headers = {
        "Host": "www.toutiao.com",
        "Connection": "keep-alive",
        "Accept": "text/javascript, text/html, application/xml, text/xml, */*",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": "http://www.toutiao.com/ch/news_tech/",
        # "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
    }
    data = {
        'category': 'news_tech',
        'utm_source': 'toutiao',
        'widen': 1,
        'max_behot_time': 0,
        'max_behot_time_tmp': 0,
        'tadrequire': True,
        'as': as_cp.get('as'),
        'cp': as_cp.get('cp'),
        '_signature': _signature,
    }

    toutiao_url = 'https://www.toutiao.com/api/pc/feed/?' + urlencode(data)
    req_obj = urllib2.Request(url=toutiao_url, headers=headers)
    req_obj = urllib2.urlopen(req_obj)

    return HttpResponse(content=req_obj.read())


def get(request):
    collection = client['ip_pool']['free_ip']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
    }

    url = 'http://www.xicidaili.com/nn/1'
    req = urllib2.Request(url, headers=headers)
    res = urllib2.urlopen(req).read()

    soup = BeautifulSoup(res)
    ips = soup.findAll('tr')

    free_ips = []
    for x in range(1, len(ips)):
        ip = ips[x]
        tds = ip.findAll("td")
        ip_temp = '%s:%s' % (tds[1].contents[0], tds[2].contents[0])

        # print tds[2].contents[0]+"\t"+tds[3].contents[0]
        free_ips.append({
            'ip': ip_temp,
            'crt': datetime.datetime.now()
        })

    collection.insert_many(free_ips)

    return JsonResponse(data=free_ips)

@csrf_exempt
@require_POST
def sett(request):
    import os
    import re
    p = os.popen(cmd)
    regex = re.compile('\s+')
    result = p.read().split('\n')[:-1]
    result = [regex.split(line)[1:] for line in result]
    return JsonResponse(data={
        'mem': dict(zip(result[0], result[1])),
        'swap': dict(zip(result[0], result[2])),
    })


def send_email(request):
    util = EmailSendUtil(host='smtp.163.com', port=25)
    from_infos = {
        'addr': 'xavierchan@163.com',
        'alias': 'xavierchan',
        'password': 'CZX521lsx'
    }
    to_infos = {
        'addr': 'zx.chen@eliteu.com.cn',
        'alias': 'zx.chen@eliteu'
    }
    email_contents = {
        'subject': 'hello',
        'content': 'hello world'
    }
    util.send_email(from_infos, to_infos, email_contents)


@login_required
def email_logs(request):
    return render(request, 'crawler/email_logs.html')


@require_GET
@login_required
def get_email_logs(request):
    page = to_int(request.GET.get('page', 1))
    page_size = to_int(request.GET.get('page_size', 20))
    status = request.GET.get('status')

    collection = client['waste_email']['logs']
    query = {} if not status else { 'status': int(status) }

    email_logs = list(collection.find(query).sort('send_time', pymongo.DESCENDING).skip((page - 1) * page_size).limit(page_size))
    for item in email_logs:
        item['_id'] = str(item['_id'])
        item['send_time'] = str(item['send_time']).split('.')[0]

    return HttpResponse(json.dumps(xresult(data={
        'list': email_logs,
        'total': collection.count()
    })), content_type='application/json')


@require_GET
@login_required
def get_statistics(request):
    collection = client['waste_email']['logs']

    success = collection.count({'status': 1})
    faile = collection.count({'status': 0})

    cfg_collection = client['waste_email']['configs']
    cfg = cfg_collection.find_one()
    cfg['_id'] = str(cfg['_id'])

    return HttpResponse(json.dumps(xresult(data={
        'total': success + faile,
        'success': success,
        'faile': faile,
        'config': cfg
    })), content_type='application/json')
