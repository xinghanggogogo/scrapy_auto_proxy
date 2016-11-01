# -*- coding: utf-8 -*-
__author__ = 'xinghang'

import  sys
reload(sys)
sys.setdefaultencoding('utf8')

import traceback
import json

from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from demo.items.tvshowItem import *
from demo.pipelines.stat import *
from demo.models.tvshowmodel import *

def format_num(num):
    return str(float(num[0:-1])*10000) if num[-1] == '万' else num

def makeurls():
    url = 'https://www.douyu.com/directory/all'
    yield url

class tvSipder(Spider):

    name = 'douyu'
    download_delay = 0.5
    allowed_domains = ["douyu.com"]

    start_urls = makeurls()

    def parse(self, response):
        print '*****************************************************'
        print response.url
        print '*****************************************************'
        staturltotal()

        sel = Selector(response)
        count = 0
        try:
            lis = sel.xpath('//*[@id="live-list-contentbox"]/li')
            for li in lis:
                count += 1
                show_img = li.xpath('a/span/img/@data-original').extract()[0].encode('utf8')

                link = li.xpath('a/@href').extract()[0].encode('utf8')
                link = '//*[@id="main_page"]/div/div[4]/div/ul/li[1]/a[1]/div[1]/img[4]' + link
                room_id = link.split('/')[-1]
                api_url = 'http://open.douyucdn.cn/api/RoomApi/room/'+room_id

                title = li.xpath('a/@title').extract()[0].encode('utf8')
                anchor = li.xpath('a/div/p/span[1]/text()').extract()[0].encode('utf8')
                category = li.xpath('a/div/div/span/text()').extract()[0].encode('utf8')

                num = li.xpath('a/div/p/span[2]/text()').extract()[0].strip()
                num = format_num(num).split('.')[0]

                meta = {
                    'show_img': show_img,
                    'link': link,
                    'title': title,
                    'anchor': anchor,
                    'category':category,
                    'num': num,
                }
                if count < 2:

                    print show_img
                    print link
                    print title
                    print anchor
                    print num
                    print ''

                    # 没有头像的进去二级链接爬取
                    try:
                        tvshow_info = tvshowModel.select().where(tvshowModel.anchor == anchor).get()
                        peewee_sql = tvshowModel.update(show_img=show_img, title=title, num=num).where(tvshowModel.anchor == tvshow_info.anchor)
                        peewee_sql.execute()
                        statsuccessitem()

                    # 有头像的更新数据
                    except:
                        yield Request(
                            url=api_url,
                            dont_filter=True,
                            callback=self.get_details,
                            meta=meta
                        )

        except Exception,e:
            print traceback.print_exc()

    def get_details(self, response):

        staturltotal()
        body = response.body_as_unicode()
        jsonobject = json.loads(body)
        data = jsonobject['data']

        item = tvshowItem()
        item['room_id'] = data['room_id']
        item['show_img'] = data['room_thumb']
        item['category'] = data['cate_name']
        item['link'] = response.meta['link']
        item['title'] = data['room_name']
        item['anchor'] = data['owner_name']
        item['head_img'] = data['avatar']
        item['source'] = 'douyu'
        item['num'] = data['online']
        item['video_link'] = 'https://staticlive.douyucdn.cn/common/share/play.swf?room_id=' + data['room_id']

        statitemtotal()

        yield item


    # def get_details(self, response):
    #
    #     print 'goto get_details'
    #     print "*****************************************************"
    #     print response.url
    #     print "*****************************************************"
    #
    #     show_img = response.meta.get('show_img')
    #     link = response.meta.get('link')
    #     title = response.meta.get('title')
    #     anchor = response.meta.get('anchor')
    #     num = response.meta.get('num')
    #     source = response.meta.get('source')
    #     category = response.meta.get('category')
    #     staturltotal()
    #     sel = Selector(response)
    #
    #     #某些活动直播头像有两种排版
    #     try:
    #         head_img = sel.xpath('//*[@id="anchor-info"]/div[1]/img/@src').extract()[0].encode('utf8')
    #     except:
    #         head_img = sel.xpath('//*[@id="live"]/div[2]/div[1]/div[3]/img/@src').extract()[0].encode('utf8')
    #     room_id = response.url.split('/')[-1]
    #     api_url = 'http://open.douyucdn.cn/api/RoomApi/room/'+room_id
    #
    #     print '\n'
    #     print show_img
    #     print link
    #     print title
    #     print anchor
    #     print category
    #     print head_img
    #     print video_link
    #     print source
    #     print num + '\n'
    #
    #     item = tvshowItem()
    #     item['show_img'] = show_img
    #     item['link'] = link
    #     item['title'] = title
    #     item['anchor'] = anchor
    #     item['category'] = category
    #     item['head_img'] = head_img
    #     item['source'] = source
    #     item['num'] = num
    #     item['video_link'] = video_link
    #
    #     statitemtotal()
    #
    #     yield item
