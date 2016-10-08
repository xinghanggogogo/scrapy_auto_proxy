# -*- coding: utf-8 -*-
__author__ = 'xinghang'

import scrapy
import time
import traceback
import random

from scrapy.selector import Selector
from scrapy.http import Request
from demo.pipelines.stat import *


class BooksSpider(scrapy.Spider):
    name = "books_des"
    pipeline = "default"
    allowed_domains = ["bookdepository.com"]
    download_delay = 2
    start_urls = ['http://www.bookdepository.com/']

    def parse(self, response):

        if response.status != 200:
            time.sleep(60)
            yield Request(response.url, meta=response.meta, callback=self.parse, dont_filter=True)


        print '0000000000000000000000000000000000'
        i = random.randint(1,3)
        time.sleep(i)
        sel = Selector(response)
        cat_st_list = sel.xpath('/html/body/div[5]/div[1]/div[1]/div/ul/li[1]')
        for i in cat_st_list:

            cat_st_name = i.xpath('a/text()').extract()[0].encode('utf8').strip()
            cat_st_link = i.xpath('a/@href').extract()[0].encode('utf8').strip()

            print 10 * '*'+'first_category'+10 * '*'
            print 'cat_st_name:'+cat_st_name
            print 'cat_st_link:'+cat_st_link
            print 10 * '*'
            print ''

            for i in range(1, 2):
                req = cat_st_link
                yield Request(req, meta={'category': cat_st_name}, callback=self.catSecondParse, dont_filter=True)
        return

    def catSecondParse(self, response):

        i = random.randint(1,3)
        time.sleep(i)

        if response.status != 200:
            time.sleep(60)
            yield Request(response.url, meta=response.meta, callback=self.catSecondParse, dont_filter=True)

        category = response.meta['category']
        sel = Selector(response)

        print 'response_url:'+response.url

        cat_sec_name = sel.xpath('//ul[@class="category-list sidebar-nav has-parent"]/li[4]/a/text()').extract()[0].encode('utf8').strip()
        cat_sec_link = sel.xpath('//ul[@class="category-list sidebar-nav has-parent"]/li[4]/a/@href').extract()[0].encode('utf8').strip()

        print 10 * '*'+'second_category'+10 * '*'
        print 'cat_nd_name:'+cat_sec_name
        print 'cat_nd_link:'+cat_sec_link
        print 10 * '*'
        print ''

        req = cat_sec_link
        yield Request(req, meta={'category':category}, callback=self.bookListParse, dont_filter=True)

        return

    # 3级目录,暂时忽略
    # def catThirdParse(self, response):
    #
    #     time.sleep(2)
    #     #访问失败
    #     if response.status != 200:
    #         time.sleep(60)
    #         yield Request(response.url, meta=response.meta, callback=self.catThirdParse, dont_filter=True)
    #
    #     sel = Selector(response)
    #     cat_rd_list = sel.xpath('/html/body/div[5]/div[1]/div[1]/div/ul/li').extract()
    #     for i in cat_rd_list[3:]:
    #
    #         cat_rd_name = i.xpath('a/text()').extract()[0].encode('utf8')
    #         cat_rd_link = i.xpath('a/@href').extract()[0].encode('utf8')
    #
    #         print 10 * '*'+'third_category'+10 * '*'
    #         print 'cat_rd_name:'+cat_rd_name
    #         print 'cat_rd_link:'+cat_rd_link
    #         print 10 * '*'
    #         print ''
    #
    #         req = cat_rd_link
    #         yield Request(req, meta={'category':cat_rd_name}, callback=self.bookListParse, dont_filter=True)
    #
    #     return

    def bookListParse(self, response):

        i = random.randint(1,3)
        time.sleep(i)

        if response.status != 200:
            time.sleep(60)
            yield Request(response.url, meta=response.meta, callback=self.bookListParse, dont_filter=True)

        category = response.meta['category']

        sel = Selector(response)
        book_list = sel.xpath('.//div[@class="book-item"]')
        for i in book_list:

            book_name = i.xpath('div[2]/h3/a/text()').extract()[0].encode('utf8').strip()
            book_link = i.xpath('div[2]/h3/a/@href').extract()[0].encode('utf8').strip()

            print '************'+'book_list'+'****************'
            print 'book_name:'+book_name
            print 'book_link:'+book_link
            print ''

            req = book_link
            yield Request(req, meta={'category':category}, callback=self.bookContentParse, dont_filter=True)

        return

    def bookContentParse(self, response):

        i = random.randint(1,3)
        time.sleep(i)

        if response.status != 200:
            time.sleep(60)
            yield Request(response.url, meta=response.meta, callback=self.catThirdParse, dont_filter=True)
        sel = Selector(response)

        category = response.meta['category']

        try:
            name = sel.xpath('//h1[@itemprop="name"]/text()').extract()[0].encode('utf8')
            img_url = sel.xpath('//img[@class="book-img"]/@src').extract()[0].encode('utf8')

            try:
                try:
                    introduction = sel.xpath('//p[@itemprop="description"]/text()').extract()[0].encode('utf8')
                except:
                    introduction = sel.xpath('//div[@class="trunc-content"]/p/text()').extract()[0].encode('utf8')
            except:
                introduction = sel.xpath('//div[@class="item-excerpt trunc"]/text()').extract()[0].encode('utf8')

            introduction = introduction.strip()

            author = sel.xpath('//div[@class="author-info hidden-md"]/a/text()').extract()[0].encode('utf8')
            author = author.strip()

            info_path = sel.xpath('//ul[@class="biblio-info"]/li')
            for item in info_path:

                key = item.xpath('label/text()').extract()[0].encode('utf8')

                if key == 'Publication date':
                    publication_date = item.xpath('span/text()').extract()[0].encode('utf8')

                if key == 'Publisher':
                    publisher = item.xpath('span/a/text()').extract()[0].encode('utf8')
                    publisher = publisher.strip()

                if key == 'Publication City/Country':
                    publication_city = item.xpath('span/text()').extract()[0].encode('utf8')
                    publication_city = publication_city.strip()

                if key == 'ISBN10':
                    isbn10 = item.xpath('span/text()').extract()[0].encode('utf8')

                if key == 'ISBN13':
                    isbn13 = item.xpath('span/text()').extract()[0].encode('utf8')

            print '***********'+'book_content'+"************"
            print 'name:' + name
            print 'img_url:' + img_url
            print 'author:' + author
            print 'category:' + category
            print 'introduction:' + introduction
            print 'publication_date:' + publication_date
            print 'publisher:' + publisher
            print 'publish_city:' + publication_city
            print 'isbn10:' + isbn10
            print 'isbn13:' + isbn13
            print ''

            # item = ebookItem()
            # item['name'] = name
            # item['img_url'] = img_url
            # item['author'] = author
            # item['category'] = category
            # item['introduction'] = introduction
            # item['publication_date'] = publication_date
            # item['publisher'] = publisher
            # item['publication_city'] = publication_city
            # item['isbn10'] = isbn10
            # item['isbn13'] = isbn13

            statitemtotal()
            # yield item

        except Exception,e:
            print traceback.print_exc()

