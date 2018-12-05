# coding: utf-8

from celery import shared_task
from models import Article
from django.db.models import F


@shared_task
def add(x, y):
    print "%d + %d = %d" % (x, y, x+y)
    return x+y


@shared_task
def mul(x, y):
    print "%d * %d = %d" % (x, y, x*y)
    return x*y


@shared_task
def sub(x, y):
    print "%d - %d = %d" % (x, y, x-y)
    return x-y


@shared_task
def increate_pv(id):
    return Article.objects.filter(id=id).update(pv=F('pv') + 1)


@shared_task
def increate_uv(id):
    return Article.objects.filter(id=id).update(uv=F('uv') + 1)
