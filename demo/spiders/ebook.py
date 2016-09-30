# -*- coding: utf-8 -*-
__author__ = 'xinghang'

import  sys
reload(sys)
sys.setdefaultencoding('utf8')
from scrapy.spiders import Spider
from scrapy.selector import Selector
import traceback
from demo.items.ebookItem import *
from demo.pipelines.stat import *
from demo.models.ebookmodel import *

def makeurls():

    for i in range(1, 52000):
        url = 'http://www.ebookdb.org/item/%s/' % i
        yield url

class hrtechchinaSipder(Spider):

    name = 'ebook'
    download_delay = 2
    allowed_domains = ["ebooksdb.org"]
    start_urls = makeurls()

    def parse(self, response):
        sel = Selector(response)
        try:
            params_path = sel.xpath('//div[@id="LayoutColumn1"]')

            name = params_path.xpath('div[2]/div[1]/div[1]/h1/text()').extract()[0].encode('utf8')
            img_url = params_path.xpath('div[2]/div[1]/div[2]/div/div/div/div[2]/img/@src').extract()[0].encode('utf8')


            author = params_path.xpath('div[2]/div[1]/div[2]/div/div/div/text()').extract()[1].encode('utf8')
            author = author.split(':')[1][1:]

            try:
                key_words = params_path.xpath('div[2]/div[1]/div[2]/div/div/div/a/text()').extract()[0].encode('utf8')
                key_words +=  params_path.xpath('div[2]/div[1]/div[2]/div/div/div/a/text()').extract()[1].encode('utf8')+' & '
                key_words +=  params_path.xpath('div[2]/div[1]/div[2]/div/div/div/a/text()').extract()[2].encode('utf8')
            except:
                pass

            category = sel.xpath('//div[1]/ul/li[2]/a/text()').extract()[0].encode('utf8')

            try:
                print '*****first_intro********'
                introduction = sel.xpath('//span[@class="isbnol_review2"]/text()').extract()[0].encode('utf8')
            except:
                print 'second_inotro'
                intrs_list = sel.xpath('//div[@class="div"]/text()').extract()
                introduction = ''
                for item in intrs_list:
                    introduction += item

            book_metas = params_path.xpath('div[2]/div[1]/div[2]/div/div/div/text()').extract()

            isbn10 = isbn13 = ''
            for item in book_metas:

                if item.split(':')[0] == 'Published':
                    publication_date = item.split(':')[1][1:]

                if item.split(':')[0] == 'Publisher':
                    publisher = item.split(':')[1][1:]

                if item.split(':')[0] == 'ISBN-10':
                    isbn10 = item.split(':')[1][1:]

                if item.split(':')[0] == 'ISBN-13':
                    isbn13 = item.split(':')[1][1:]

            # publisher = params_path.xpath('div[2]/div[1]/div[2]/div/div/div/text()').extract()
            # publisher = publisher.split(':')[1][1:]

            # publication_date = params_path.xpath('div[2]/div[1]/div[2]/div/div/div/text()').extract()
            # publication_date = publication_date.split(':')[1][1:]

            # key = params_path.xpath('div[2]/div[1]/div[2]/div/div/div/text()').extract()[8].encode('utf8')

            # print 10 * '*'
            # print (key)
            # print 10 * '*'
            #
            # if key == 'eBookDB-ID':
            #     pass
            # else:
            #     isbn10 = params_path.xpath('div[2]/div[1]/div[2]/div/div/div/text()').extract()[8].encode('utf8')
            #     isbn13 = params_path.xpath('div[2]/div[1]/div[2]/div/div/div/text()').extract()[9].encode('utf8')
            #
            #     isbn10 = isbn10.split(':')[1][1:]
            #     isbn13 = isbn13.split(':')[1][1:]

            lis = params_path.xpath('div[2]/div[1]/div[4]/div[1]/ul')
            link = ''
            print "********************pre***********************"
            for li in lis:
                try:
                    link = li.xpath('li/a/@href').extract()[0].encode('utf8')
                    if link != '/':
                        print "********************first***********************"
                        link = link
                        break #action
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

            print response.url
            print name
            print img_url
            print author
            print key_words
            print category
            print introduction
            print publisher
            print publication_date
            print isbn10
            print isbn13
            print 'link:' + link
            print 'linkd_online:' + link_online
            print 'link_pdf:' + link_pdf
            print 'link_txt:' + link_txt
            print 20 * "*"

            # book_info = ebookModel.select().where(ebookModel.isbn10 == '0751561460').get()
            # print 10 * '*'
            # print book_info.category
            # print 10 * '*'
            #
            # if category:
            #     category =  category + ' & ' + book_info.category
            #
            # peewee_sql = ebookModel.update(key_words=key_words, category=category, link_usual=link_usual).where(ebookModel.isbn10 == '0751561460')
            # peewee_sql.execute()

            item = ebookItem()
            item['name'] = name
            item['img_url'] = img_url
            item['key_words'] = key_words
            item['author'] = author
            item['category'] = category
            item['key_words'] = key_words
            item['introduction'] = introduction
            item['publication_date'] = publication_date
            item['publisher'] = publisher
            item['isbn10'] = isbn10
            item['isbn13'] = isbn13
            item['link_usual'] = link
            item['link_pdf'] = link_pdf
            item['link_online'] = link_online
            item['link_txt'] = link_txt

            statitemtotal()
            yield item

        except Exception,e:
            print traceback.print_exc()

