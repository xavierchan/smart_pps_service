# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import base64
import hmac
import json
import logging
import random
import urllib
import urllib2
import uuid
from hashlib import sha1 as sha

import datetime
import rsa
import time
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from aliyun_oss.models import OssFile
from common.oss_util import OssUtil
from smart_pps_service.common.common import AuthUtils
from smart_pps_service.common.common import xresult, get_real_ip, md_2_html


logger = logging.getLogger('oss')

oss_util = OssUtil(
    access_key_id=settings.ALIYUN.get('AccessKeyId', ''),
    access_key_secret=settings.ALIYUN.get('AccessKeySecret', ''),
    endpoint=settings.ALIYUN.get('oss').get('Endpoint'),
    buckets=settings.ALIYUN.get('oss').get('Buckets')
)


@csrf_exempt
def upload(request):
    '''
    ```
    file = request.FILES.get('upload_file')
    url = 'http://127.0.0.1:8300/aliyun_oss/upload/'
    data = {
        'system': 'support',
        'customer': '1'
    }
    files = {
        'upload_file': (
            file.name, file.read(), file.content_type
        )
    }
    res = requests.post(url, data=data, files=files)
    return HttpResponse(res, content_type='application/json')
    :param request: 
    :return: 
    '''
    try:
        start_time = datetime.datetime.now()
        envs = {
            'dev': 0,
            'beta': 1,
            'demo': 2,
            'prod': 3
        }
        env = 'dev'
        remote_ip = request.META.get('HTTP_X_FORWARDED_FOR') if request.META.has_key(
            'HTTP_X_FORWARDED_FOR') else request.META.get('REMOTE_ADDR')
        remote_ip = remote_ip.split(',')[0] if len(remote_ip.split(',')) > 0 else remote_ip
        if settings.EDUCATION and settings.EDUCATION.get('ip_envs') and settings.EDUCATION.get('ip_envs').get(
                remote_ip):
            env = settings.EDUCATION.get('ip_envs').get(remote_ip)
        file = request.FILES.get('upload_file')
        file_name = '{timestamp}{random_num}.{ext}'.format(
            timestamp=datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S'),
            random_num=''.join(random.sample([str(n) for n in xrange(10)], 4)),
            ext=file.name.split('.', 1)[1]
        )

        key = oss_util.create_key(
            env=env,
            system=request.POST.get('system') if request.POST.get('system') else 'other',
            customer=request.POST.get('customer') if request.POST.get('customer') else 'other',
            file_name=file_name
        )
        result = oss_util.put_object(file, key)
        file_like = oss_util.get_object(key)
        oss_file = OssFile.objects.create(
            env=envs[env],
            system=request.POST.get('system') if request.POST.get('system') else 'other',
            uploader_id=request.POST.get('customer') if request.POST.get('customer') else 'other',
            name=file.name,
            size=file_like.content_length,
            type=file_like.content_type,
            key=key,
            fid=str(uuid.uuid1()),
            upload_ip=remote_ip
        )
        file_url = '/oss_media/%s' % oss_file.fid
        return HttpResponse(json.dumps({
            'code': '200',
            'detail': file_url,
            'msg': ''
        }), content_type='application/json')
    except Exception as e:
        logger.error(str(e))
        return HttpResponse(json.dumps(failed_result(msg=str(e))), content_type='application/json')


def get_iso_8601(expire):
    return datetime.datetime.fromtimestamp(expire).isoformat() + 'Z'


@csrf_exempt
def get_upload_policy(request):
    '''
    获取上传策略
    :param request: 
    :return: 
    '''
    # 参数
    mode = request.POST.get('mode', 'prod')
    system = request.POST.get('system')
    user = request.POST.get('user')

    # 域名白名单
    req_ip = get_real_ip(request)
    req_origin = request.META.get('HTTP_ORIGIN')

    # if mode == 'prod' and not (
    #                 req_ip in settings.EDUCATION.get('ip_envs').keys() or req_origin in settings.EDUCATION.get(
    #             'whilelist')):
    #     return HttpResponse(json.dumps(xresult(msg='Unauthorized Request')))
    # env = 'dev/' if req_ip not in settings.EDUCATION.get('ip_envs').keys() else settings.EDUCATION.get('ip_envs').get(
    #     req_ip) + '/'

    # 参数
    access_key_id = settings.ALIYUN.get('AccessKeyId', '')
    access_key_secret = settings.ALIYUN.get('AccessKeySecret', '')
    bucket = settings.ALIYUN.get('oss', {}).get('Buckets', [''])[0]
    endpoint = settings.ALIYUN.get('oss', {}).get('Endpoint', '')
    host = 'http://%s.%s' % (bucket, endpoint)
    expire_time = settings.ALIYUN.get('oss', {}).get('ExpireTime', 30)
    upload_dir = 'dev/'

    expire_syncpoint = int(time.time()) + expire_time
    expire = get_iso_8601(expire_syncpoint)
    policy_encode = base64.b64encode(json.dumps({
        'expiration': expire,
        'conditions': [
            ['starts-with', '$key', upload_dir]
        ]
    }).strip())
    h = hmac.new(access_key_secret, policy_encode, sha)
    sign_result = base64.encodestring(h.digest()).strip()
    base64_callback_body = base64.b64encode(json.dumps({
        'callbackUrl': '%s/aliyun_oss/notify' % settings.SYSTEM.get('DOMAIN', ''),
        'callbackBody': 'filename=${object}&size=${size}&mimeType=${mimeType}' +
                        '&system={system}&user={user}&req_ip={req_ip}'.format(system=system, user=user,
                                                                              req_ip=req_ip) + '&originName=${x:originname}',
        'callbackBodyType': 'application/x-www-form-urlencoded',
    }).strip());

    token_dict = {
        'accessid': access_key_id,
        'host': host,
        'dir': upload_dir,
        'expire': expire_syncpoint,
        'policy': policy_encode,
        'signature': sign_result,
        'callback': base64_callback_body
    }
    response = HttpResponse(json.dumps(xresult(data=token_dict)), content_type='application/json')
    response['Access-Control-Allow-Methods'] = 'POST'
    response['Access-Control-Allow-Origin'] = '*'
    return response


@csrf_exempt
def notify(request):
    '''

    :param request: 
    :return: 
    '''
    # get public key
    pub_key_url = ''
    try:
        pub_key_url_base64 = request.META['HTTP_X_OSS_PUB_KEY_URL']
        pub_key_url = pub_key_url_base64.decode('base64')
        url_reader = urllib2.urlopen(pub_key_url)
        pub_key = url_reader.read()
    except Exception as e:
        print 'pub_key_url : ' + pub_key_url
        print 'Get pub key failed!'
        return HttpResponse(status=400)

    # get authorization
    authorization_base64 = request.META['HTTP_AUTHORIZATION']
    authorization = authorization_base64.decode('base64')

    # get callback body
    callback_body = request.body

    # compose authorization string
    auth_str = ''
    pos = request.path.find('?')
    if -1 == pos:
        auth_str = request.path + '\n' + callback_body
    else:
        auth_str = urllib2.unquote(request.path[0:pos]) + request.path[pos:] + '\n' + callback_body
    print auth_str

    # verify authorization
    try:
        rsa_pub = rsa.PublicKey.load_pkcs1_openssl_pem(pub_key)
        result = rsa.verify(auth_str, authorization, rsa_pub)
    except Exception as e:
        result = False

    if not result:
        print 'Authorization verify failed!'
        print 'Public key : %s' % (pub_key)
        print 'Auth string : %s' % (auth_str)
        return HttpResponse(status=400)

    # do something accoding to callback_bodytemplates
    fid = str(uuid.uuid1())
    oss_file = OssFile.objects.create(
        uploader_id=request.POST.get('user'),
        name=request.POST.get('originName'),
        size=request.POST.get('size'),
        type=request.POST.get('mimeType'),
        key=request.POST.get('filename'),
        fid=fid,
        upload_ip=request.POST.get('req_ip')
    )

    return HttpResponse(json.dumps(xresult(data={
        'fid': fid,
        'object': request.POST.get('filename'),
        'origin_name': request.POST.get('originName'),
        'mime_type': request.POST.get('mimeType'),
        'size': request.POST.get('size')
    })))


def read(request, fid=None):
    # 参数
    is_download = request.GET.get('is_download', '')
    is_download = True if is_download and str(is_download) == '1' else False
    # 获取对象key
    try:
        oss_file = OssFile.objects.get(fid=fid)
        key = oss_file.key
        filename = oss_file.name
    except Exception as e:
        # TODO 加日志记录
        pass
    if is_download:
        file_like = oss_util.get_object(key)
        response = HttpResponse(file_like, content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment;filename=' + urllib.quote(filename.encode('utf-8'))
        response['Content-Length'] = file_like.content_length
    else:
        query_string = '' if len(request.META['QUERY_STRING']) == 0 else '?' + request.META['QUERY_STRING']
        response = HttpResponseRedirect(
            'https://{bucket}.{endpoint}/{key}{query_string}'.format(
                bucket=settings.ALIYUN.get('oss').get('Buckets')[0],
                endpoint=settings.ALIYUN.get('oss').get('Endpoint'),
                key=oss_file.key,
                query_string=query_string
            )
        )
        # response = HttpResponse(file_like, content_type=file_like.content_type)
    return response


@csrf_exempt
@require_http_methods(["DELETE"])
@AuthUtils.auth_check
def del_object(request, fid=''):
    oss_object = OssFile.objects.filter(fid=str(fid)).first()
    try:
        result = oss_util.del_object(oss_object.key)
        if result.status != 204:
            raise Exception('del error, please check oss service')
        oss_object.delete()
        response = HttpResponse(json.dumps(true_result()))
    except Exception as e:
        response = HttpResponse(json.dumps(failed_result()))
    return response


@csrf_exempt
@require_http_methods(["POST"])
@AuthUtils.auth_check
def batch_del_objects(request):
    fids = request.POST.get('fids')
    oss_objs = OssFile.objects.filter(fid__in=fids)
    try:
        result = oss_util.batch_del_objects(oss_objs.values('key'))
        if result.status != 204:
            raise Exception('del error, please check oss service')
        oss_objs.delete()
        response = HttpResponse(json.dumps(true_result()))
    except Exception as e:
        response = HttpResponse(json.dumps(failed_result()))
    return response


# @csrf_exempt
# @AuthUtils.auth_check
def file_list(request):
    paginator = Paginator(OssFile.objects.all(), 10)

    return JsonResponse(xresult(data={
        'list': [obj for obj in paginator.page(1).object_list.values('id', 'fid', 'key', 'name', 'type')]
    }))


def api_docs(request):
    '''
    接口文档
    :param request: 
    :return: 
    '''
    html5_content = md_2_html(settings.BASE_DIR + '/docs/aliyun_oss.md')
    return render(request, 'dataflow/api_docs.html', {
        'docs_content': html5_content.replace('<table>', '<table class="table">')
    })


@csrf_exempt
@require_http_methods(["GET"])
def get_upload_sts(request):
    # 获取参数
    access_key_id = request.GET.get('access_key_id', '')
    access_key_secret = request.GET.get('access_key_secret', '')
    DurationSeconds = request.GET.get('duration', '')

    # 角色的全局资源描述符
    role_arn = request.GET.get('role_arn', 'acs:ram::1781958873169801:role/aliyunosstokengeneratorrole')

    # 会话名称
    # 用户自定义参数。此参数用来区分不同的Token，可用于用户级别的访问审计
    role_session_name = 'mobile'

    # 构建一个 Aliyun Client, 用于发起请求
    # 构建Aliyun Client时需要设置AccessKeyId和AccessKeySevcret
    REGIONID = 'cn-shenzhen'
    ENDPOINT = 'sts.cn-shenzhen.aliyuncs.com'

    # 配置要访问的STS Endpoint
    region_provider.add_endpoint('Sts', REGIONID, ENDPOINT)
    # 初始化Client
    clt = client.AcsClient(access_key_id, access_key_secret, REGIONID)

    # 构造"AssumeRole"请求
    request = AssumeRoleRequest.AssumeRoleRequest()
    # 指定角色
    request.set_RoleArn(role_arn)
    # 设置会话名称，审计服务使用此名称区分调用者
    request.set_RoleSessionName(role_session_name)

    # 设置会话过期时间
    if DurationSeconds:
        request.set_DurationSeconds(DurationSeconds)

    # 发起请求，并得到response
    response = clt.do_action_with_exception(request)
    return HttpResponse(response, content_type='application/json')


@csrf_exempt
@require_http_methods(["POST"])
def app_callback(request):
    fid = str(uuid.uuid1())

    envs = ['dev', 'beta', 'demo', 'prod']

    filename = request.body
    args = filename.split('/')

    try:
        OssFile.objects.create(
            env=envs.index(args[0], 0),
            system=args[1],
            uploader_id=args[2],
            name=request.POST.get('originName', ''),
            size=request.POST.get('size', ''),
            type=request.POST.get('mimeType', ''),
            key=filename,
            fid=fid,
            upload_ip=request.POST.get('req_ip', '')
        )

    except Exception as ex:
        logger.error(ex)
        return HttpResponse(json.dumps(failed_result(msg='failed')))

    return HttpResponse(json.dumps(true_result(data={
        'fid': '/oss_media/' + fid,
        'domain': 'https://bss.eliteu.cn',
    })))


def file_upload(request):
    return render(request, 'aliyun_oss/uploader.html')


@login_required
def list(request):
    return render(request, 'aliyun_oss/list.html')


@login_required
def index(request):
    return render(request, 'aliyun_oss/index.html')
