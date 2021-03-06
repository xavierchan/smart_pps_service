# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from smart_pps_service.common.common import xresult
from blog.models import Article


def index(request):
    num = 5
    spead_articles = Article.objects.filter(is_published=True, is_recommend=True).order_by('crt')
    latest = spead_articles[:num].only('id', 'title', 'upt', 'pv')
    return render(request, 'index.html', {
        'latest_articles': latest
    })


@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        req_params = json.loads(request.body)
        username = req_params.get('username')
        password = req_params.get('password')

        try:
            user = authenticate(username=username, password=password, request=request)
        except Exception as ex:
            pass

        # login
        try:
            login(request, user)
            if request.POST.get('remember') == 'true':
                request.session.set_expiry(604800)
            else:
                request.session.set_expiry(0)
            response = xresult(msg='login success', data='/')
        except Exception as ex:
            response = xresult(code=-1)

        return JsonResponse(response)

    return render(request, 'login.html')


@csrf_exempt
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


@login_required
def manage(request):
    return render(request, 'manage.html')


def proj(request):
    return render(request, 'proj.html')


def plan(request):
    return render(request, 'plan.html')


def about(request):
    return render(request, 'about.html')


def page_not_found(request):
    return render_to_response('404.html')


def page_error(request):
    return render_to_response('500.html')

