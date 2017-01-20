# -*- coding: utf-8 -*-
__author__ = 'xinghang'

import  sys
reload(sys)
sys.setdefaultencoding('utf8')

import traceback
import json
from scrapy.selector import Selector


from scrapy.spiders import Spider
from demo.items.tvshowItem import *
from demo.pipelines.stat import *
from demo.models.tvshowmodel import *

def format_num(num):
    return str(float(num[0:-1])*10000) if num[-1] == '万' else num

def makeurls():
    url = 'https://www.zhanqi.tv/api/static/v2.1/live/list/10/1.json'
    yield url

class TvSipder(Spider):

    name = 'zhanqi'
    download_delay = 0.5
    allowed_domains = ["zhanqi.com"]

    start_urls = makeurls()

    def parse(self, response):
        try:
            staturltotal()
            body = response.body_as_unicode()
            jsonobject = json.loads(body)
            res = jsonobject['data']['rooms']
            count = 0
            for data in res:

                if count < 2:
                    count += 1
                    item = tvshowItem()
                    item['room_id'] = data['id']
                    item['show_img'] = data['bpic']
                    item['category'] = data['gameName']
                    item['link'] = 'http://www.quanmin.tv/v/' + data['uid']
                    item['title'] = data['title']
                    item['anchor'] = data['nickname']
                    item['head_img'] = data['avatar']
                    item['source'] = 'zhanqi'
                    item['num'] = data['online']
                    item['video_link'] = 'http://www.zhanqi.tv/live/embed?roomId=' + data['id']

                    try:
                        #之前获取或该房间的信息,更新重要字段
                        tvshow_info = tvshowModel.select().where(tvshowModel.anchor == data['nick']).get()
                        peewee_sql = tvshowModel.update(show_img=item['show_img'], title=item['title'],
                                                        num=item['num']).where(tvshowModel.anchor == tvshow_info.anchor)
                        peewee_sql.execute()
                        statsuccessitem()

                    except:
                        #首次爬取
                        statitemtotal()
                        yield item

        except:
            print traceback.print_exc()
