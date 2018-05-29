# coding: utf-8
# @Time    : 2018/5/28 20:05
# @Author  : xavier

import urllib2
import json


class ApiStore(object):
    '''
    Api工具
    单例模式
    '''
    __instance = None
    __first_init = True

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls, *args, **kwargs)
        return cls.__instance

    def query_id_card(self, id):
        url = 'http://a.apix.cn/tongyu/idcardinfo/id?id=%s' % id
        headers = {
            'accept': "application/json",
            'content-type': "application/json",
            'apix-key': "您的apix-key"
        }
        req_obj = urllib2.Request(url, headers)
        req_obj = urllib2.urlopen(req_obj)
        res = json.loads(req_obj.read())
        return res

if __name__ == '__main__':
    api = ApiStore()
    print api.query_id_card('441900199208200873')