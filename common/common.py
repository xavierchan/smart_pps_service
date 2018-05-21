# coding: utf-8
# @Time    : 2018/5/16 21:11
# @Author  : xavier

import hashlib
import urllib2
import time
import datetime
import json

from django.http import HttpResponse
from django.conf import settings


class AuthUtils(object):
    """
    认证工具
    """
    __app_id = settings.AUTH_TOKEN.get('APP_ID')
    __pwd = settings.AUTH_TOKEN.get('SECRET')

    @classmethod
    def __get_token(cls, timestamp, data={}):
        string = '%s%s%s%s' % (cls.__app_id, cls.__pwd, timestamp, json.dumps(data))
        token = hashlib.new("md5", string.encode('utf-8')).hexdigest()
        return token

    @classmethod
    def create_token(cls, data={}):
        timestamp = str(time.mktime(datetime.datetime.now().timetuple())).split('.')[0]
        string = '%s%s%s%s' % (cls.__app_id, cls.__pwd, timestamp, json.dumps(data))
        token = hashlib.new("md5", string.encode('utf-8')).hexdigest()
        return (token, timestamp)

    @classmethod
    def post_json(cls, url, data={}):
        token, timestamp = cls.create_token(data)
        headers = {
            'content-type': 'application/json',
            'timestamp': timestamp,
            'token': token
        }
        req_obj = urllib2.Request(url=url, headers=headers, data=json.dumps(data))
        res = urllib2.urlopen(req_obj)
        res_content = res.read()
        res = json.loads(res_content)
        return res

    @classmethod
    def auth_check(cls, func):
        def before(request, *args, **kwargs):
            timestamp = request.META.get('HTTP_TIMESTAMP')
            org_token = request.META.get('HTTP_TOKEN')
            if not timestamp or not org_token:
                return HttpResponse(content=json.dumps({
                    'code': '500',
                    'detail': None,
                    'msg': '拒绝非法访问'
                }), content_type='application/json')
            token = cls.__get_token(timestamp, json.loads(request.body))
            if token != org_token:
                return HttpResponse(content=json.dumps({
                    'code': '500',
                    'detail': None,
                    'msg': '认证失败'
                }), content_type='application/json')
            return func(request, *args, **kwargs)
        return before


class ReUtils(object):
    @classmethod
    def is_mobile(cls):
        pass


def get_real_ip(request):
    remote_ip = request.META.get('HTTP_X_FORWARDED_FOR') if request.META.has_key(
        'HTTP_X_FORWARDED_FOR') else request.META.get('REMOTE_ADDR')
    remote_ip = remote_ip.split(',')[0] if len(remote_ip.split(',')) > 0 else remote_ip
    return remote_ip


def xresult(code=0, msg='', data=None):
    # TODO 异常错误补充
    ERROR_CODES = {}
    msg = ERROR_CODES.get(code) if ERROR_CODES.has_key(code) else msg

    return {
        'code': code,
        'data': data,
        'msg': msg
    }
