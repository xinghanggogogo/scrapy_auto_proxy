# -*- coding: utf-8 -*-
__author__ = 'xinghang'

import  sys
reload(sys)
sys.setdefaultencoding('utf8')
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import Request
import traceback
from demo.items.nameItem import *
from demo.pipelines.stat import *

def makeurls():
    word_list = [chr(i).upper() for i in range(97, 123)]
    for word in word_list:
        for page in range(1,2):
            url = 'http://ename.dict.cn/list/all/%s/%s'% (word, page)
            yield url

class thundernamesSipder(Spider):

    name = 'thundernames'
    #download_delay = 0.5
    allowed_domains = ["ename.dict.cn"]

    start_urls = makeurls()
    #start_urls = ['http://ename.dict.cn/list/all/A/1']

    def parse(self, response):
        print '*****************************************************'
        print response.url
        print '*****************************************************'
        staturltotal()

        sel = Selector(response)

        try:
            lis = sel.xpath('//tr')
            for li in lis:
                try:
                    ename = li.xpath('td[1]/a/text()').extract()[0].encode('utf8')
                    gender = li.xpath('td[2]/em/@title').extract()[0].encode('utf8')
                    sounce = li.xpath('td[3]/i/text()').extract()[0].encode('utf8')
                    cname= li.xpath('td[4]/text()').extract()[0].encode('utf8')
                    source = li.xpath('td[5]/bdo/text()').extract()[0].encode('utf8')
                    hot_level = li.xpath('td[6]/span/@class').extract()[0].encode('utf8')

                    detail_link = li.xpath('td[1]/a/@href').extract()[0].encode('utf8')
                    detail_link= 'http://ename.dict.cn'+detail_link

                    meta = {
                        'ename': ename,
                        'gender': gender,
                        'sounce': sounce,
                        'cname': cname,
                        'source': source,
                        'hot_level': hot_level,
                        'detail_link': detail_link
                    }

                    print detail_link

                    yield Request(
                        url=detail_link,
                        dont_filter=True,
                        callback=self.get_details,
                        meta=meta
                    )
                except:
                    pass

        except Exception,e:
            print traceback.print_exc()

    def get_details(self, response):

        print 'goto get_details'
        print "*****************************************************"
        print response.url
        print "*****************************************************"

        ename = response.meta.get('ename')
        gender= response.meta.get('gender')
        sounce = response.meta.get('sounce')
        cname = response.meta.get('cname')
        source = response.meta.get('source')
        hot_level = response.meta.get('hot_level')
        detail_link = response.meta.get('detail_link')

        staturltotal()
        sel = Selector(response)

        try:
            detailsPATH = sel.xpath('//ul')
            detail = detailsPATH.xpath('//li[2]/span/text()').extract()[0].encode('utf8')
        except:
            detail = ''
            print traceback.print_exc()

        masterstr = ''
        try:
            mastersPATH = sel.xpath('//div[@class="forname"]/ul/li')
            for masterPATH in mastersPATH:
                master = masterPATH.xpath('text()').extract()[0].encode('utf8') + masterPATH.xpath('text()').extract()[1].encode('utf8')
                print 'master:%s' % master
                masterstr +=master + '&'
        except:
            print traceback.print_exc()

        print ename
        print gender
        print sounce
        print cname
        print source
        print hot_level
        print detail_link
        print detail
        print masterstr

        if gender=='男性' or gender == '中性':
            gender = 'boy'
        else:
            gender = 'girl'



        item = nameItem()
        item['ename'] = ename
        item['gender'] = gender
        item['sounce'] = sounce
        item['cname'] = cname
        item['source'] = source
        item['hot_level'] = hot_level
        item['detail_link'] = detail_link
        item['detail'] = detail
        item['masters'] = masterstr

        statitemtotal()
        yield item
