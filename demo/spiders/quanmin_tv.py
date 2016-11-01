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
    url = 'http://www.quanmin.tv/json/play/list.json'
    yield url

class TvSipder(Spider):

    name = 'quanmin'
    download_delay = 0.5
    allowed_domains = ["quanmin.com"]
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
                    item['room_id'] = data['uid']
                    item['show_img'] = data['thumb']
                    item['category'] = data['category_name']
                    item['link'] = 'http://www.quanmin.tv/v/'+data['uid']
                    item['title'] = data['title']
                    item['anchor'] = data['nick']
                    item['head_img'] = data['avatar']
                    item['source'] = 'quanmin'
                    item['num'] = data['view']
                    item['video_link'] = 'http://www.quanmin.tv/yileyou/' + data['uid']

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
