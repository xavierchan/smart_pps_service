# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import urllib2

from django.conf import settings
from django.contrib.auth.models import User
from django.http.response import JsonResponse
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings

from member.models import MemberProfile
from smart_pps_service.common.common import xresult

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class LoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        # params
        miniapp_settings = settings.WECHAT.get('MINIAPP', {})
        js_code = json.loads(request.body).get('code')

        url = 'https://api.weixin.qq.com/sns/jscode2session?appid={app_id}&secret={secret}&js_code={js_code}' \
              '&grant_type=authorization_code'.format(
            app_id=miniapp_settings.get('APPID'),
            secret=miniapp_settings.get('SECRET'),
            js_code=js_code,
        )
        # get wechat
        req_obj = urllib2.urlopen(url=url)
        res = json.loads(req_obj.read())

        # 判断
        if res.has_key('errcode'):
            pass
            response = xresult(code=-1)
        else:
            if MemberProfile.objects.filter(wx_open_id=res.get('openid')).exists():
                member_profile = MemberProfile.objects.filter(wx_open_id=res.get('openid')).first()
                member = member_profile.member
            else:
                member = User()
                member.save()
                member_profile = MemberProfile(wx_open_id=res.get('openid'), wx_union_id=res.get('unionid', ''), member=member)
                member_profile.save({ 'wx_open_id': res.get('openid') })

            payload = jwt_payload_handler(member)
            token = jwt_encode_handler(payload)

            response = xresult(data=token)

        return JsonResponse(response)
