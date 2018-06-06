# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
import top.api


class TestApi(TestCase):

    def setUp(self):
        pass


    def test_api(self):
        req = top.api.TbkItemGetRequest(url, port)
        req.set_app_info(top.appinfo(appkey, secret))

        req.fields = "num_iid,title,pict_url,small_images,reserve_price,zk_final_price,user_type,provcity,item_url,seller_id,volume,nick"
        req.q = "女装"
        req.cat = "16,18"
        req.itemloc = "杭州"
        req.sort = "tk_rate_des"
        req.is_tmall = False
        req.is_overseas = False
        req.start_price = 10
        req.end_price = 10
        req.start_tk_rate = 123
        req.end_tk_rate = 123
        req.platform = 1
        req.page_no = 123
        req.page_size = 20
        try:
            resp = req.getResponse()
            print(resp)
        except Exception, e:
            print(e)


    def tearDown(self):
        pass

