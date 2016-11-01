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
    url = 'http://live.bilibili.com/area/liveList?area=all&order=online&page=1'
    yield url

class TvSipder(Spider):

    name = 'bzhan'
    download_delay = 0.5
    allowed_domains = ["bilibili.com"]
    start_urls = makeurls()

    def parse(self, response):
        try:
            staturltotal()
            body = response.body_as_unicode()
            jsonobject = json.loads(body)
            res = jsonobject['data']
            count = 0
            for data in res:

                if count < 2:

                    count += 1
                    item = tvshowItem()
                    item['room_id'] = data['roomid']
                    item['show_img'] = data['cover']
                    item['category'] = data['areaName']
                    item['link'] = 'http://live.bilibili.com' + data['link']
                    item['title'] = data['title']
                    item['anchor'] = data['uname']
                    item['head_img'] = data['face']
                    item['source'] = 'bzhan'
                    item['num'] = data['online']
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
