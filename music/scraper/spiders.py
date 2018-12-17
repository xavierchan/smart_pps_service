# coding: utf-8

from dynamic_scraper.spiders.django_spider import DjangoSpider
from music.models import MusicsWebsite, CMusic, CMusicItem


class MucisSpider(DjangoSpider):

    name = 'cmusic_spider'

    def __init__(self, *args, **kwargs):
        self._set_ref_object(MusicsWebsite, **kwargs)
        self.scraper = self.ref_object.scraper
        self.scrape_url = self.ref_object.url
        self.scheduler_runtime = self.ref_object.scraper_runtime
        self.scraped_obj_class = CMusic
        self.scraped_obj_item_class = CMusicItem
        super(MucisSpider, self).__init__(self, *args, **kwargs)
