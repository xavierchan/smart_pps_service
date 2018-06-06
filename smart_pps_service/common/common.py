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
from markdown import markdown


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


def md_2_html(md_path):
    docs_content = open(md_path).read()
    html5_content = markdown(
        docs_content,
        output_format='html5',
        extensions=[
            'markdown.extensions.toc',
            WikiLinkExtension(base_url='https://en.wikipedia.org/wiki/',
                              end_url='#Hyperlinks_in_wikis'),
            'markdown.extensions.sane_lists',
            'markdown.extensions.codehilite',
            'markdown.extensions.abbr',
            'markdown.extensions.attr_list',
            'markdown.extensions.def_list',
            'markdown.extensions.fenced_code',
            'markdown.extensions.footnotes',
            'markdown.extensions.smart_strong',
            'markdown.extensions.meta',
            'markdown.extensions.nl2br',
            'markdown.extensions.tables'
        ]
    )
    return html5_content


def md_2_html2(docs_content):
    html5_content = markdown(
        docs_content,
        output_format='html5',
        extensions=[
            'markdown.extensions.toc',
            'markdown.extensions.sane_lists',
            'markdown.extensions.codehilite',
            'markdown.extensions.abbr',
            'markdown.extensions.attr_list',
            'markdown.extensions.def_list',
            'markdown.extensions.fenced_code',
            'markdown.extensions.footnotes',
            'markdown.extensions.smart_strong',
            'markdown.extensions.meta',
            'markdown.extensions.nl2br',
            'markdown.extensions.tables'
        ]
    )
    return html5_content


def xresult(code=0, msg='', data=None):
    # TODO 异常错误补充
    ERROR_CODES = {}
    msg = ERROR_CODES.get(code) if ERROR_CODES.has_key(code) else msg

    return {
        'code': code,
        'data': data,
        'msg': msg
    }


def get_int(values, key, default=0):
    value = values.get(key)
    if value:
        value = int(value)
    else:
        value = default
    return value
