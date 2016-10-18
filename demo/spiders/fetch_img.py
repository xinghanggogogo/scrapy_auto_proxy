# -*- coding: utf-8 -*-
__author__ = 'xinghang'

import  sys
reload(sys)
sys.setdefaultencoding('utf8')
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from demo.models.ebookmodel import *
import traceback
from demo.pipelines.stat import *


class oneSipder(Spider):

    name = 'fetch_img'
    download_delay = 1.1
    allowed_domains = ["amazon.com"]
    def start_requests(self):
        books_info = ebookModel.select()
        for book_info in books_info:
            if book_info.img_url == '':
                isbn10 = book_info.isbn10
                url = 'https://www.amazon.com/exec/obidos/ASIN/%s/isbncheckcom-20' % isbn10
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
            print ''
            print img_url
            print ''

            #更新数据库
            isbn10 = response.meta['isbn10']
            peewee_sql = ebookModel.update(img_url=img_url).where(ebookModel.isbn10 == isbn10)
            peewee_sql.execute()

        except Exception,e:
            print traceback.print_exc()
