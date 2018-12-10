# coding: utf-8

import json

from celery import shared_task
from models import Comic, ComicChapter
from crawlers.crawler import QQComicCrawler


@shared_task
def crawle_qq_comic(id):
    crawler = QQComicCrawler()
    c_info = crawler.get_info(id)
    comic = Comic.objects.create(name=c_info.get('name'),
                                 author=c_info.get('author'),
                                 cover=c_info.get('cover'),
                                 intro=c_info.get('intro'),
                                 ac_id=id
                                 )
    for bc in c_info.get('chapters')[:1]:
        for c in bc.get('chapters')[:4]:
            crawle_qq_comic_pic.delay(id, c.get('cid'), c.get('title'))
    return comic


@shared_task
def crawle_qq_comic_pic(id, cid, title):
    crawler = QQComicCrawler()
    comic = Comic.objects.filter(ac_id=id).first()
    c_chapter = crawler.get_chapter(id, cid)
    comic_chapter = ComicChapter.objects.create(
        comic=comic,
        ac_cid=cid,
        chapter=cid,
        title=title,
        imgs=json.dumps(c_chapter.get('imgs'))
    )
    return comic_chapter
