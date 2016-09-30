# -*- coding: utf-8 -*-
__author__ = 'xinghang'

import scrapy
import time
from scrapy.selector import Selector
from scrapy.http import Request


class BooksSpider(scrapy.Spider):
    name = "amazon"
    pipeline = "default"
    allowed_domains = ["amazon.cn"]
    download_delay = 2

    start_urls = (
        'https://www.amazon.cn/%E5%9B%BE%E4%B9%A6/b/ref=topnav_storetab_b?ie=UTF8&node=658390051',
    )

    def parse(self, response):

        time.sleep(2)

        #访问失败,status ！= 200,再次请求
        if response.status != 200:
            time.sleep(60)
            yield Request(response.url, meta=response.meta, callback=self.parse, dont_filter=True)

        self.pipeline = "booksType"
        sel = Selector(response)
        a_list = sel.xpath('.//div[@class="categoryRefinementsSection"]/ul[1]/li/a[1]')

        for a in a_list:

            #item = AmazonBooksTypeItem()
            type_name = a.xpath('span[1]/text()').extract()[0].encode('utf8')
            type_book_num = a.xpath('span[2]/text()').extract()[0].encode('utf8')
            type_link = a.xpath('@href[1]').extract()[0].encode('utf8')

            print 10 * '*'+'bookstart'
            print type_name + type_book_num + type_link
            print 10 * '*'
            print ''

            # item['typeName'] = [n.encode('utf-8') for n in name]
            # item['typeNum'] = [n.encode('utf-8') for n in num]
            # item['typeLink'] = [n.encode('utf-8') for n in link]
            # yield AmazonBooksTypeItem(item)

            #按照page爬取book_list
            for i in range(1, 2): #max=75
                req = type_link + '&page=' + str(i)
                yield Request(req, callback=self.booksListParse, dont_filter=True)
        return

    def booksListParse(self, response):

        time.sleep(2)
        #访问失败, 再次请求
        if response.status != 200:
            time.sleep(60)
            yield Request(response.url, meta=response.meta, callback=self.booksListParse, dont_filter=True)

        self.pipeline = "booksList"
        sel = Selector(response)
        list = sel.xpath('.//div[@id="mainResults"]/ul/li/div/div/div/div[2]')

        for i in list:
            #item = AmazonBooksListItem()
            book_name = i.xpath('div[2]/a/@title').extract()[0].encode('utf8')
            book_link = i.xpath('div[2]/a/@href').extract()[0].encode('utf8')
            author = i.xpath('div[2]/div/span[2]/text()').extract()[0].encode('utf8')

            #有的图书没有第二作者,这里会报错吗
            author2 = i.xpath('div[2]/div/span[3]/text()').extract()
            #author2 = i.xpath('div[2]/div/span[3]/text()').extract()[0].encode('utf8')

            publication_date= i.xpath('div[2]/span[3]/text()').extract()[0].encode('utf8')
            price = i.xpath('div[3]/div[1]/div[2]/a/span/text()').extract()[0].encode('utf8')
            hot_level = i.xpath('div[3]/div[2]/div/span/span/a/i[1]/span/text()').extract()[0].encode('utf8')

            print 10 * '*'+'booklist'
            print 'book_list_book_name:'+book_name
            print 'book_list_book_link:'+book_link
            print 10 * '*'
            print ''

            # item['bookName'] = [n.encode('utf-8') for n in name]
            # item['bookAuthor'] = [n.encode('utf-8') for n in author]
            # item['bookAuthor2'] = [n.encode('utf-8') for n in author2]
            # item['bookTime'] = [n.encode('utf-8') for n in time]
            # item['bookPrice'] = [n.encode('utf-8') for n in price]
            # item['bookStar'] = [n.encode('utf-8') for n in star]
            # item['bookLink'] = [n.encode('utf-8') for n in link]
            # yield AmazonBooksListItem(item)

            req = book_link
            yield Request(req, meta={'bookName': book_name}, callback=self.bookContentParse, dont_filter=True)

        return

    def bookContentParse(self, response):

        time.sleep(2)
        #访问失败
        if response.status != 200:
            time.sleep(60)
            yield Request(response.url, meta=response.meta, callback=self.bookContentParse, dont_filter=True)

        self.pipeline = "bookContent"
        sel = Selector(response)
        bookName = response.meta['bookName']

        #这是一个list
        introduction = sel.xpath('.//*[@id="iframeContent"]').extract()
        if len(introduction) < 1:
            introduction = sel.xpath('.//*[@id="bookDescription_feature_div"]/noscript/div').extract()
        introduction = introduction[0].encode('utf8')

        comment_link = sel.xpath('.//div[@id="revSum"]/div[2]/div/div[1]/a/@href').extract()[0].encode('utf8')
        commentnum = sel.xpath('.//div[@id="revF"]/div/a/text()').extract()[0].encode('utf8')

        #取出数字
        comment_num = ''
        for i in range(len(commentnum[0])):
            if '0' <= commentnum[0][i] <= '9':
                comment_num += commentnum[0][i]

        print 10 * '*'+'bookcontent'
        print 'book_content_book_name:' + bookName
        print 'book_content_book_introductio' + introduction
        print 'book_content_comment_link:' + comment_link
        print 'book_content_comment_num:' + comment_num
        print 10 * '*'
        print ''

        # item = AmazonBookContentItem()
        # item['bookName'] = bookName
        # item['bookContent'] = [n.encode('utf-8') for n in content]
        # item['bookCommentUrl'] = [n.encode('utf-8') for n in commenturl]
        # item['bookCommentNum'] = commentNum
        # yield AmazonBookContentItem(item)

        try:
            pageNum = (int(comment_num) / 10) + 1
            for i in range(1, pageNum):
                req = comment_link[0] + '?pageNumber=' + str(i)
                yield Request(req, meta={'bookName': bookName}, callback=self.bookCommentParse, dont_filter=True)
        except:
            pass
        return

    def bookCommentParse(self, response):

        time.sleep(2)
        #访问失败
        if response.status != 200:
            time.sleep(60)
            yield Request(response.url, meta=response.meta, callback=self.bookCommentParse, dont_filter=True)

        self.pipeline = "bookComment"
        sel = Selector(response)
        comment_list = sel.xpath('.//div[@id="cm_cr-review_list"]/div')

        for i in comment_list:

            comment_star = i.xpath('div[1]/a[1]/i/span/text()').extract()[0].encode('utf8')
            comment_title = i.xpath('div[1]/a[2]/text()').extract().extract[0].encode('utf8')
            comment_time = i.xpath('div[2]/span[4]/text()').extract()[0].encode('utf8')
            content = i.xpath('div[4]/span/text()').extract()[0].encode('utf8')

            print 10 * '*'+'bookcomment'
            print 'book_comment_star:'+comment_star
            print 'book_comment_title:'+comment_title
            print 'book_comment_time'+comment_time
            print 'book_comment_content'+content
            print 10 * '*'

            # item = AmazonBookCommentItem()
            # item['bookName'] = response.meta['bookName']
            # item['bookCommentStar'] = [n.encode('utf-8') for n in star]
            # item['bookCommentTitle'] = [n.encode('utf-8') for n in title]
            # item['bookCommentTime'] = [n.encode('utf-8') for n in time]
            # item['bookCommentContent'] = [n.encode('utf-8') for n in content]
            # yield AmazonBookCommentItem(item)







# import traceback
# import  sys
# reload(sys)
# sys.setdefaultencoding('utf8')
#
# from scrapy.selector import Selector
# from scrapy.spiders import CrawlSpider, Rule
# from scrapy.linkextractors import LinkExtractor as sle
# from demo.items.ebookItem import *
# from demo.pipelines.stat import *
#
#
# class amazonbookSpider(CrawlSpider):
#     name = "amazon"
#     allowed_domains = ["amazon.com"]
#     start_urls = [
#         "https://www.amazon.com",
#     ]
#
#     rules = [
#         Rule(sle(allow=("/.*$")), callback='getBookMeta', follow=True),
#     ]
#
#     def getBookMeta(self, response):
#
#         print 10 * '!@#$'
#         print response.url

        # print response.url
        # sel = Selector(response)
        # try:
        #     name = sel.xpath('//h1[@itemprop="name"]/text()').extract()[0].encode('utf8')
        #     img_url = sel.xpath('//img[@class="book-img"]/@src').extract()[0].encode('utf8')
        #
        #     try:
        #         introduction = sel.xpath('//p[@itemprop="description"]/text()').extract()[0].encode('utf8')
        #     except:
        #         introduction = sel.xpath('//div[@class="trunc-content"]/p/text()').extract()[0].encode('utf8')
        #     introduction = introduction.strip()
        #
        #     author = sel.xpath('//div[@class="author-info"]/a/text()').extract()[0].encode('utf8')
        #     author = author.strip()
        #
        #     try:
        #         category = sel.xpath('//ol[@class="breadcrumb"]/li[3]/text()').extract()[0].encode('utf8')
        #     except:
        #         category = ''
        #
        #     info_path = sel.xpath('//ul[@class="biblio-info"]/li')
        #     for item in info_path:
        #
        #         key = item.xpath('label/text()').extract()[0].encode('utf8')
        #
        #         if key == 'Publication date':
        #             publication_date = item.xpath('span/text()').extract()[0].encode('utf8')
        #
        #         if key == 'Publisher':
        #             publisher = item.xpath('span/a/text()').extract()[0].encode('utf8')
        #             publisher = publisher.strip()
        #
        #         if key == 'Publication City/Country':
        #             publication_city = item.xpath('span/text()').extract()[0].encode('utf8')
        #             publication_city = publication_city.strip()
        #
        #         if key == 'ISBN10':
        #             isbn10 = item.xpath('span/text()').extract()[0].encode('utf8')
        #
        #         if key == 'ISBN13':
        #             isbn13 = item.xpath('span/text()').extract()[0].encode('utf8')
        #
        #     # try:
        #     #     test = int(isbn10)
        #     #     print test
        #     # except:
        #     #     isbn10 = sel.xpath('//ul[@class="biblio-info"]/li[7]/span/text()').extract()[0].encode('utf8')
        #     #     isbn13 = sel.xpath('//ul[@class="biblio-info"]/li[8]/span/text()').extract()[0].encode('utf8')
        #
        #     print 'name:' + name
        #     print 'img_url:' + img_url
        #     print 'author:' + author
        #     print 'category:' + category
        #     print 'introduction:' + introduction
        #     print 'publication_date:' + publication_date
        #     print 'publisher:' + publisher
        #     print 'publish_city:' + publication_city
        #     print 'isbn10:' + isbn10
        #     print 'isbn13:' + isbn13
        #
        #     item = ebookItem()
        #
        #     item['name'] = name
        #     item['img_url'] = img_url
        #     item['author'] = author
        #     item['category'] = category
        #     item['introduction'] = introduction
        #     item['publication_date'] = publication_date
        #     item['publisher'] = publisher
        #     item['publication_city'] = publication_city
        #     item['isbn10'] = isbn10
        #     item['isbn13'] = isbn13
        #
        #     statitemtotal()
        #     yield item
        #
        # except Exception,e:
        #     print traceback.print_exc()
