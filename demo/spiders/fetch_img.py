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


class oneSipder(Spider):

    name = 'fetch_img'
    allowed_domains = ["amazon.com"]
    def start_requests(self):
        books_info = ebookModel.select().where(ebookModel.img_url == '')
        for book_info in books_info:
            isbn10 = book_info.isbn10
            url = 'https://www.amazon.com/exec/obidos/ASIN/%s/isbncheckcom-20' % isbn10

            i = random.randint(1, 3)
            time.sleep(i)

            yield Request(
                url,
                headers={ 'Referer': 'https://www.amazon.com' },
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
            img_url = sel.xpath('//*[@id="imgBlkFront"]/@src').extract()[0].encode('utf8')
            isbn10 = response.meta['isbn10']
            peewee_sql = ebookModel.update(img_url=img_url).where(ebookModel.isbn10 == isbn10)
            peewee_sql.execute()

            print ''
            print 'update success!'
            print img_url
            print ''

        except Exception,e:
            print traceback.print_exc()
