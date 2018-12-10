# coding: utf-8

import requests
import time
import os

from bs4 import BeautifulSoup
from django.conf import settings

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


requestSession = requests.session()
# Chrome on win10
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
requestSession.headers.update({'User-Agent': UA})


class QQComicCrawler(object):

    def get_info(self, id):
        info_url = 'https://ac.qq.com/Comic/comicInfo/id/{id}'.format(id=id)
        html_doc = requestSession.get(info_url).text
        soup = BeautifulSoup(html_doc, 'html.parser')

        season_chapters = []
        for k in soup.select('.works-chapter-list-wr'):
            chapters = [{
                'title': item.text.strip(),
                'cid': item.get('href').split('/')[-1]
              } for item in k.select('.works-chapter-item a')]
            season_chapters.append({
                'title': '',
                'chapters': chapters
            })
        return {
            'cover': soup.select('.works-cover img')[0].get('src', ''),
            'name': soup.select('.works-intro-title strong')[0].text,
            'author': soup.select('.works-intro-digi .first em')[0].text.strip(),
            'intro': soup.select('.works-intro-short')[0].text.strip(),
            'chapters': season_chapters
        }

    def get_chapter(self, id, cid):
        chapter_url = 'https://ac.qq.com/ComicView/index/id/{id}/cid/{cid}'.format(id=id, cid=cid)

        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        # base_path = '/Users/liying/Documents/xavier/newwp/smart_pps_service'
        driver_path = os.path.join(settings.BASE_DIR, 'comic/driver/chromedriver')
        browser = webdriver.Chrome(executable_path=driver_path, chrome_options=chrome_options)
        browser.get(chapter_url)

        html_doc = browser.page_source
        soup = BeautifulSoup(html_doc, 'html.parser')
        page_count = len(soup.select('#comicContain')[0].select('li'))
        for i in xrange(page_count):
            height = i * 970
            js = 'document.getElementById("mainView").scrollTo({}, {})'.format(height, height + 970)
            browser.execute_script(js)
            time.sleep(0.1)

        html_doc = browser.page_source
        soup = BeautifulSoup(html_doc, 'html.parser')
        container = soup.select('#comicContain')[0]

        imgs = [(li.span.text if li.span else '', li.img.get('src')) for li in container.select('li') if str(li.img.get('src')).startswith('https://manhua.qpic.cn/manhua_detail')]
        imgs = [img[1] for img in imgs]
        return {
            'page': container.select('.comic-text')[0].select('em')[0].text,
            'imgs': imgs
        }


if __name__ == '__main__':
    id = '505430'
    cid = 1
    c = QQComicCrawler()
    # c_info = c.get_info(id)
    c_chapters = c.get_chapter(id, cid)
