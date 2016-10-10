# -*- coding: utf-8 -*-
__author__ = 'xinghang'

import  sys
reload(sys)
sys.setdefaultencoding('utf8')
from scrapy.spiders import Spider
from scrapy.selector import Selector
import traceback
from scrapy.http import Request

from demo.items.ebookItem import *
from demo.pipelines.stat import *

from ghost import Ghost
from scrapy import log
import re
class Cookieutil:

    def __init__(self,url):
        log.msg('init cookieutil class ,will be get %s cookie information!' %url, log.INFO)
        gh = Ghost(download_images=False,display=False)
        gh.open(url)
        gh.open(url)
        gh.save_cookies("cookie.txt")
        gh.exit()

    def getCookie(self):
        cookie = ''
        with open("cookie.txt") as f:
            temp = f.readlines()
            for index in temp:
                cookie += self.parse_oneline(index).replace('\"','')
        return cookie[:-1]

    def parse_oneline(self,src):
        oneline = ''
        if re.search("Set-Cookie",src):
            oneline = src.split(';')[0].split(':')[-1].strip()+';'
        return oneline


class gudenbargSipder(Spider):

    name = 'gudenbarg'
    download_delay = 5
    allowed_domains = ["gudenberg.org"]

    def star_urls(self):
        res = []
        for i in range(52271, 52272):
            url = 'http://www.gutenberg.org/ebooks/53149'
            res.append(url)
        return res

    def start_requests(self):
        urls = self.star_urls()
        print urls
        for url in urls:
            yield Request(url, cookies={'session_id': 'b909dc6990dc1edc957ca3d00d4bc170783cdb8d',
                                        'bonus': 'id7668'})

    def parse(self, response):
        sel = Selector(response)
        try:

            name = sel.xpath('//div[@class="header"]h1/text()').extract()[0].encode('utf8')
            img_url = sel.xpath('//img[@class="cover-art"]/@src').extract()[0].encode('utf8')

            author = sel.xpath('//tbody/tr[1]/td/text()').extract()[0].encode('utf8')
            category = sel.xpath('//tbody/tr[4]/td/text()').extract()[0].encode('utf8')
            public_time = sel.xpath('//tbody/tr[6]/td/text()').extract()[0].encode('utf8')
            public_house = sel.xpath('//tbody/tr[7]/td/text()').extract()[0].encode('utf8')

            # isbn10 = params_path.xpath('div[2]/div[1]/div[2]/div/div/div/text()').extract()[8].encode('utf8')[9:]
            # isbn13 = params_path.xpath('div[2]/div[1]/div[2]/div/div/div/text()').extract()[9].encode('utf8')[9:]

            print name
            print img_url
            print author
            print category
            print public_house
            print public_time

            item = ebookItem()
            #statitemtotal()
            #yield item

        except Exception,e:
            print traceback.print_exc()

