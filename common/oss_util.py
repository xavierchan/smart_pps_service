# coding: utf-8
# @Time    : 2018/1/11 10:39
# @Author  : xavier


from django.conf import settings

import oss2
from itertools import islice


class OssUtil(object):
    '''
    阿里云对象存储(OSS)工具
    单例模式
    '''
    __instance = None
    __first_init = True

    def __init__(self, *args, **kwargs):
        if self.__class__.__first_init:
            access_key_id = kwargs.get('access_key_id', '')
            access_key_secret = kwargs.get('access_key_secret', '')
            self.endpoint = kwargs.get('endpoint', '')
            self.auth = oss2.Auth(access_key_id, access_key_secret)
            # self.__service = oss2.Service(self.__endpoint)
            self.buckets = kwargs.get('buckets', [])

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls, *args, **kwargs)
        return cls.__instance

    def __get_bucket(self):
        return oss2.Bucket(self.auth, self.endpoint, self.buckets[0])

    def put_bucket(self):
        pass

    def put_object(self, file, key):
        return self.__get_bucket().put_object(data=file.chunks(), key=key)

    def get_object(self, key):
        return self.__get_bucket().get_object(key=key)

    def list_object(self, size):
        return [obj for obj in islice(oss2.ObjectIterator(self.__get_bucket()), size)]

    def create_key(self, **kwargs):
        key = '{env}/{system}/{customer}/{file_name}'.format(
            env=kwargs.get('env'),
            system=kwargs.get('system'),
            customer=kwargs.get('customer'),
            file_name=kwargs.get('file_name')
        )
        return key

