# -*- coding: utf-8 -*-
__author__ = 'xinghang'

import  sys
reload(sys)
sys.setdefaultencoding('utf8')
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import Request
import traceback
#from demo.items.oneItem import *
from demo.pipelines.stat import *

def makeurls():
    for one in range(1, 1486):
        url = 'http://wufazhuce.com/one/%s' % one
        yield url

class oneSipder(Spider):

    name = 'one'
    download_delay = 0.5
    allowed_domains = ["wufazhuce.com"]

    start_urls = makeurls()

    def parse(self, response):
        print '*****************************************************'
        print response.url
        print '*****************************************************'
        staturltotal()

        sel = Selector(response)

        try:
            img_url = sel.xpath('.//div[@class="one-imagen"]/img/@src').extract()[0].encode('utf8')
            img_author = sel.xpath('.//div[@class="one-imagen-leyenda"]/text()').extract()[0].encode('utf8').strip()
            text = sel.xpath('.//div[@class="one-cita"]/text()').extract()[0].encode('utf8').strip()

            print ''
            print img_url
            print img_author
            print text
            print ''

            # item = oneItem
            # item['img_url'] = img_url
            # item['img_author'] = img_author
            # item['text'] = text
            # yield item

        except Exception,e:
            print traceback.print_exc()
