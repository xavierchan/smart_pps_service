# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response


@login_required
def index(request):
    return render_to_response('ai/index.html')


def face_recognite(request):
    return render_to_response('ai/face_recognite.html')
