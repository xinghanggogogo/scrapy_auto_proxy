# -*- coding: utf-8 -*-
__author__ = 'xinghang'

import scrapy
import time
import random
from scrapy.selector import Selector
from scrapy.http import Request


class BooksSpider(scrapy.Spider):
    name = "amazon_us"
    pipeline = "default"
    allowed_domains = ["amazon.com"]
    download_delay = 2

    start_urls = (
        'https://www.amazon.com/books-used-books-textbooks/b/ref=nav_shopall_bo?ie=UTF8&node=283155',
    )

    def parse(self, response):

        if response.status != 200:
            time.sleep(60)
            yield Request(response.url, meta=response.meta, callback=self.parse, dont_filter=True)

        self.pipeline = "booksType"
        sel = Selector(response)
        a_list = sel.xpath('.//div[@class="categoryRefinementsSection"]/ul[1]/li/a[1]')

        for a in a_list:

            type_name = a.xpath('span[1]/text()').extract()[0].encode('utf8')
            type_book_num = a.xpath('span[2]/text()').extract()[0].encode('utf8')
            type_link = a.xpath('@href[1]').extract()[0].encode('utf8')

            print 10 * '*'+'bookstart'
            print type_name + type_book_num + type_link
            print 10 * '*'
            print ''

            #item = AmazonBooksTypeItem()
            # item['typeName'] = [n.encode('utf-8') for n in name]
            # item['typeNum'] = [n.encode('utf-8') for n in num]
            # item['typeLink'] = [n.encode('utf-8') for n in link]
            # yield AmazonBooksTypeItem(item)

            #按照page爬取book_list
            for i in range(1, 2): #max=5000
                req = type_link + '&page=' + str(i)
                yield Request(req, meta={'category':type_name}, callback=self.booksListParse, dont_filter=True)
        return

    def booksListParse(self, response):

        i = random.randint(1,3)
        time.sleep(i)

        if response.status != 200:
            time.sleep(60)
            yield Request(response.url, meta=response.meta, callback=self.booksListParse, dont_filter=True)

        self.pipeline = "booksList"
        category = response.meta['category']
        sel = Selector(response)
        list = sel.xpath('.//div[@id="mainResults"]/ul/li/div/div/div/div[2]')

        for i in list[0:1]:
            book_name = i.xpath('div[2]/a/@title').extract()[0].encode('utf8')
            book_link = i.xpath('div[2]/a/@href').extract()[0].encode('utf8')
            img_url = sel.xpath('.//div[@id="mainResults"]/ul/li/div/div/div/div[1]/div/div/a/img/@src').extract()[0].encode('utf8')

            try:
                author = i.xpath('div[2]/div/span[2]/a/text()').extract()[0].encode('utf8')
            except:
                author = i.xpath('div[2]/div/span[2]/text()').extract()[0].encode('utf8')

            #暂时忽略第二作者
            #author2 = i.xpath('div[2]/div/span[3]/a/text()').extract()
            #author2 = i.xpath('div[2]/div/span[3]/text()').extract()[0].encode('utf8')

            date= i.xpath('div[2]/span[3]/text()').extract()[0].encode('utf8')

            try:
                price = i.xpath('div[3]/div[1]/div[2]/a/span/text()').extract()[0].encode('utf8')
            except:
                price = ''

            try:
                hot_level = i.xpath('div[3]/div[2]/div/span/span/a/i[1]/span/text()').extract()[0].encode('utf8')
            except:
                hot_level = ''

            print 10 * '*'+'booklist'
            print 'book_list_book_name:'+book_name
            print 'book_list_book_author:'+author
            print 'book_list_book_link:'+book_link
            print 'book_list_book_img:'+img_url
            print 'book_list_book_price:'+price
            print 'book_list_book_hot_level:'+hot_level
            print 'book_list_book_pbdata:'+date
            print 10 * '*'
            print ''

            # item = AmazonBooksListItem()
            # item['bookName'] = [n.encode('utf-8') for n in name]
            # item['bookAuthor'] = [n.encode('utf-8') for n in author]
            # item['bookAuthor2'] = [n.encode('utf-8') for n in author2]
            # item['bookTime'] = [n.encode('utf-8') for n in time]
            # item['bookPrice'] = [n.encode('utf-8') for n in price]
            # item['bookStar'] = [n.encode('utf-8') for n in star]
            # item['bookLink'] = [n.encode('utf-8') for n in link]
            # yield AmazonBooksListItem(item)

            req = book_link
            yield Request(req,
                          meta={'name': book_name, 'author': author, 'link': book_link, 'price': price, 'hot_level': hot_level, 'date': date, 'img_url': img_url, 'category':category},
                          callback=self.bookContentParse,
                          dont_filter=True)

        return

    def bookContentParse(self, response):

        i = random.randint(1,3)
        time.sleep(i)

        if response.status != 200:
            time.sleep(60)
            yield Request(response.url, meta=response.meta, callback=self.bookContentParse, dont_filter=True)

        self.pipeline = "bookContent"
        sel = Selector(response)

        name = response.meta['name']
        author = response.meta['author']
        category = response.meta['category'].lower() # 格式处理
        book_link = response.meta['link']
        img_url = response.meta['img_url']
        price = response.meta['price']
        hot_level = response.meta['hot_level']
        publication_date = response.meta['date']

        info_path = sel.xpath('.//*[@id="productDetailsTable"]/tr/td/div[1]/ul/li')
        for i in info_path:
            key = i.xpath('b/text()').extract()[0].encode('utf8')[:-1]
            #print key

            if key == 'Publisher':
                publisher = i.xpath('text()').extract()[0].encode('utf8').split('(')[0][1:-1]

            if key == 'ISBN-10':
                #严格处理isbn10：
                isbn10 = ''
                isbn10_get = i.xpath('text()').extract()[0].encode('utf8')
                for i in range(len(isbn10_get)):
                    if '0' <= isbn10_get[i] <= '9' or isbn10_get[i] in ['-', 'x', 'X']:
                        isbn10 += isbn10_get[i]

            if key == 'ISBN-13':
                #严格处理isbn13：
                isbn13 = ''
                isbn13_get = i.xpath('text()').extract()[0].encode('utf8')
                for i in range(len(isbn13_get)):
                    if '0' <= isbn13_get[i] <= '9' or isbn13_get[i] in ['-', 'x', 'X']:
                        isbn13 += isbn13_get[i]

        #这是一个list
        introduction = sel.xpath('//*[@id="iframeContent"]/p[1]/span/text()').extract()
        if len(introduction) < 1:
            introduction = sel.xpath('.//*[@id="bookDescription_feature_div"]/noscript/div').extract()
        introduction = introduction[0].encode('utf8')

        comment_link = sel.xpath('.//div[@id="revSum"]/div[2]/div/div[1]/a/@href').extract()[0].encode('utf8')

        print 10 * '*'+'bookcontent'
        print 'content_book_name:' + name
        print 'content_book_author:' + author
        print 'content_book_link:' + book_link
        print 'content_book_img:' + img_url
        print 'content_book_category' + category
        print 'content_book_price:' + price
        print 'content_book_hot:' + hot_level
        print 'content_book_introduction' + introduction
        print 'content_book_date:' + publication_date
        print 'content_book_publisher：'+ publisher
        print 'content_book_isbn10:' + isbn10
        print 'content_book_isbn13:' + isbn13
        print 'content_comment_link:' + comment_link
        print 10 * '*'
        print ''

        # item = ebookItem()
        # item['name'] = name
        # item['img_url'] = img_url
        # item['author'] = author
        # item['category'] = category
        # item['introduction'] = introduction
        # item['publication_date'] = publication_date
        # item['publisher'] = publisher
        # item['isbn10'] = isbn10
        # item['isbn13'] = isbn13

        # statitemtotal()
        # yield item

        try:
            req = comment_link
            yield Request(req, meta={'bookName': name}, callback=self.bookCommentParse, dont_filter=True)
        except:
            pass

        return

    def bookCommentParse(self, response):

        i = random.randint(1,3)
        time.sleep(i)

        if response.status != 200:
            time.sleep(60)
            yield Request(response.url, meta=response.meta, callback=self.bookCommentParse, dont_filter=True)

        sel = Selector(response)

        comment_list = sel.xpath('//div[@class="a-section review"]')

        for i in comment_list:

            comment_title = i.xpath('div[1]/a[2]/text()').extract()[0].encode('utf8')
            comment_time = i.xpath('div[2]/span[4]/text()').extract()[0].encode('utf8')
            content = i.xpath('div[4]/span/text()').extract()[0].encode('utf8')

            print ''
            print 10 * '*'+'bookcomment'
            print 'book_comment_title:'+comment_title
            print 'book_comment_time'+comment_time
            print 'book_comment_content'+content
            print 10 * '*'
            print ''

            # item = AmazonBookCommentItem()
            # item['bookName'] = response.meta['bookName']
            # item['bookCommentStar'] = [n.encode('utf-8') for n in star]
            # item['bookCommentTitle'] = [n.encode('utf-8') for n in title]
            # item['bookCommentTime'] = [n.encode('utf-8') for n in time]
            # item['bookCommentContent'] = [n.encode('utf-8') for n in content]
            # yield AmazonBookCommentItem(item)
