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
    url = 'http://www.huomao.com/channels/channel.json?page=1&page_size=10&cache_time=1477987230&game_url_rule=all'
    yield url

class TvSipder(Spider):

    name = 'huomao'
    download_delay = 0.5
    allowed_domains = ["huomao.com"]
    start_urls = makeurls()

    def parse(self, response):
        try:
            staturltotal()
            body = response.body_as_unicode()
            jsonobject = json.loads(body)
            res = jsonobject['data']['channelList']
            count = 0
            for data in res:

                if count < 2:

                    count += 1
                    item = tvshowItem()
                    item['room_id'] = data['room_number']
                    item['show_img'] = data['image']
                    item['category'] = data['gameCname']
                    item['link'] = 'http://www.huomao.com/'+data['room_number']
                    item['title'] = data['channel']
                    item['anchor'] = data['nickname']
                    item['head_img'] = data['headimg']['big']
                    item['source'] = 'huomao'
                    item['num'] = data['originviews']
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
