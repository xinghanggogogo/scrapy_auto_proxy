#coding:utf-8

import scrapy
import traceback

from scrapy.http import Request
from scrapy.selector import Selector
from demo.items.proxyItem import *
class XiciProxySpider(scrapy.Spider):

    name = 'xici_proxy'
    allowed_domains = ['xicidaili.com']

    def start_requests(self):
        url = 'http://www.xicidaili.com/nn'
        yield Request(
            url,
            headers={
                'Referer': 'http://www.xicidaili.com',
                'Accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, * / *;q = 0.8',
                'Accept - Encoding':'gzip, deflate, sdch',
                'Accept - Language':'zh - CN, zh;q = 0.8',
                'Cache - Control':'max - age = 0',
                'Connection':'keep - alive',
                'Host':'www.xicidaili.com',
                'Upgrade - Insecure - Requests': 1,
                'User - Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'
            },
            cookies={
                '_free_proxy_session':'BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJTJkZjI5ZmZmNDQ3YTExOGYwOWU0ZjEwNTcwMjVjODUwBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMXZnaGNiSTlKL1ljRlIvbmZxZy9RM1pUTkZMS1JBNEJweklSUGdTOEp5TnM9BjsARg%3D%3D--0014aec3aa990caddce02a312f5546de7328a37c',
                'CNZZDATA1256960793':'211163373-1476428933-null%7C1476428933'
            },
            callback=self.parse_item
        )


    def parse_item(self, response):

        sel = Selector(response)

        trs = sel.xpath('.//tr[@class="odd" or @class=""]')
        for tr in trs:
            try:
                ip = tr.xpath('td[2]/text()').extract()[0].encode('utf8')
                port = tr.xpath('td[3]/text()').extract()[0].encode('utf8')

                print ip
                print port

            except:
                print traceback.print_exc()


class ProxySpider360(scrapy.Spider):

    name = '360_proxy'
    allowed_domains = ['www.proxy360.cn']

    def start_requests(self):
        url = 'http://www.proxy360.cn/default.aspx'
        yield Request(
            url,
            callback=self.parse_item
        )

    def parse_item(self, response):

        sel = Selector(response)

        trs = sel.xpath('.//div[@class="proxylistitem"]')
        for tr in trs:
            try:

                ip = tr.xpath('div[1]/span/text()').extract()[0].encode('utf8').strip()
                port = tr.xpath('div[1]/span/text()').extract()[1].encode('utf8').strip()

                print ip
                print port

                item = proxyItem()
                item['ip'] = ip
                item['port'] = port

                yield item

            except:
                print traceback.print_exc()
