# -*- coding: utf-8 -*-
__author__ = 'xinghang'

import  sys
reload(sys)
sys.setdefaultencoding('utf8')

import json
import traceback

from scrapy.spiders import Spider
from demo.items.tvshowItem import *
from demo.pipelines.stat import *
from demo.models.tvshowmodel import *

def makeurls():
    url = 'http://api.plu.cn/tga/streams?max-results=18&start-index=54&sort-by=views&filter=0&game=0'
    yield url

class TvSipder(Spider):

    name = 'longzhu'
    download_delay = 0.5
    allowed_domains = ["longzhu.com"]
    start_urls = makeurls()

    def parse(self, response):
        try:
            staturltotal()
            body = response.body_as_unicode()
            jsonobject = json.loads(body)
            res = jsonobject['data']['items']
            count = 0
            for data in res:

                if count < 2:

                    count += 1
                    item = tvshowItem()
                    item['room_id'] = data['channel']['id']
                    item['show_img'] = data['preview']
                    item['category'] = data['game'][0]['Name']
                    item['link'] = data['channel']['url']
                    item['title'] = data['channel']['status']
                    item['anchor'] = data['channel']['name']
                    item['head_img'] = data['channel']['avatar']
                    item['source'] = 'longzhu'
                    item['num'] = data['viewers']
                    item['video_link'] = ''

                    try:
                        tvshow_info = tvshowModel.select().where(tvshowModel.anchor == data['nick']).get()
                        peewee_sql = tvshowModel.update(show_img=item['show_img'], title=item['title'], num=item['num']).where(tvshowModel.anchor == tvshow_info.anchor)
                        peewee_sql.execute()
                        statsuccessitem()

                    except:
                        statitemtotal()
                        yield item

        except:
            print traceback.print_exc()
