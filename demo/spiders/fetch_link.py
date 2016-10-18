# -*- coding: utf-8 -*-
__author__ = 'xinghang'

import  sys
reload(sys)
import traceback
import time
import random

sys.setdefaultencoding('utf8')
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from demo.models.ebookmodel import *
from demo.pipelines.stat import *


class fetch1Sipder(Spider):

    name = 'fetch_link'
    allowed_domains = ["openisbn.com"]
    def start_requests(self):
        books_info = ebookModel.select()
        for book_info in books_info:
            isbn10 = book_info.isbn10
            url = 'http://www.openisbn.com/isbn/%s/' % isbn10

            yield Request(
                url,
                headers={ 'Referer': 'http://www.openisbn.com' },
                callback=self.parse_item,
                meta={'isbn10':isbn10}
            )


    def parse_item(self, response):

        print '*****************************************************'
        print response.url
        print '*****************************************************'
        staturltotal()

        sel = Selector(response)

        try:
            links = sel.xpath('//div[@class="ArticleExtra"]/ul/li/a/@href').extract()
            for link in links:
                key = link.encode('utf8')[-3:]
                print '*******************key*********************'
                print key
                print '*******************key*********************'

                if key == 'txt':
                    link_txt = 'http://www.openisbn.com'+link
                if key == 'tml':
                    link_online = 'http://www.openisbn.com'+link

                try:
                    if not link_pdf:
                        pass
                except:
                    link_pdf = ''

                try:
                    if not link_txt:
                        pass
                except:
                    link_txt = ''

                try:
                    if not link_online:
                        pass
                except:
                    link_online = ''

                if link_online or link_pdf or link_txt:

                    isbn10 = response.meta['isbn10']
                    peewee_sql = ebookModel.update(link_txt=link_txt, link_online=link_online).where((ebookModel.isbn10 == isbn10))
                    peewee_sql.execute()

                    print ''
                    print 'update success!'
                    print ''

        except Exception,e:
            print '此站未能更新'


class fetch2Sipder(Spider):

    name = 'fetch_link2'
    allowed_domains = ["ebooksdb.org"]

    def start_requests(self):
        for i in range(1, 54776):
            url = 'http://www.ebookdb.org/item/%s/' % i
            yield Request(
                url,
                headers={ 'Referer': 'http://www.ebookdb.org/' },
                callback=self.parse_item,
            )

    def parse_item(self, response):
        sel = Selector(response)
        try:
            params_path = sel.xpath('//div[@id="LayoutColumn1"]')
            lis = params_path.xpath('div[2]/div[1]/div[4]/div[1]/ul')
            link = ''
            print "********************pre***********************"
            for li in lis:
                try:
                    link = li.xpath('li/a/@href').extract()[0].encode('utf8')
                    if link != '/':
                        print "********************first***********************"
                        link = link
                        break
                except:
                    pass

            if not link:
                print "***********************second**************************"
                lis = params_path.xpath('div[2]/div[2]/div[1]/ul')
                for li in lis:
                    link = li.xpath('li/a/@href').extract()[0].encode('utf8')
                    if link != '/':
                        link = link

            link_online = ''
            if link[0] == '/':
                link_online = 'http://www.ebookdb.org' + link

            link_pdf = ''
            if link[-3:] == 'pdf':
                link_pdf = link

            link_txt = ''
            if link[-3:] == 'txt':
                link_txt = link

            book_metas = params_path.xpath('div[2]/div[1]/div[2]/div/div/div/text()').extract()

            for item in book_metas:
                if item.split(':')[0] == 'ISBN-10':
                    isbn10 = item.split(':')[1][1:]

            peewee_sql = ebookModel.update(link_pdf=link_pdf, link_txt=link_txt,
                                           link_online=link_online).where((ebookModel.isbn10 == isbn10))
            peewee_sql.execute()

            print ''
            print 'update success!'
            print ''

        except Exception,e:
            print traceback.print_exc()
            print '此站未能更新'
