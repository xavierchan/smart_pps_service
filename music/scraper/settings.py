# coding: utf-8

import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smart_pps_service.settings") #Changed in DDS v.0.3

BOT_NAME = 'music'

LOG_STDOUT = False
LOG_LEVEL = 'INFO'

SPIDER_MODULES = ['dynamic_scraper.spiders', 'music.scraper', ]
USER_AGENT = '%s/%s' % (BOT_NAME, '1.0')

ITEM_PIPELINES = {
    'dynamic_scraper.pipelines.DjangoImagesPipeline': 200,
    'dynamic_scraper.pipelines.ValidationPipeline': 400,
    'music.scraper.pipelines.DjangoWriterPipeline': 800,
}

# IMAGES_STORE = os.path.join(PROJECT_ROOT, '/media/thumbnails')
#
# IMAGES_THUMBS = {
#     'medium': (50, 50),
#     'small': (25, 25),
# }

DSCRAPER_IMAGES_STORE_FORMAT = 'ALL'

DSCRAPER_LOG_ENABLED = True
DSCRAPER_LOG_LEVEL = 'ERROR'
DSCRAPER_LOG_LIMIT = 5
