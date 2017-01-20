# -*- coding: utf-8 -*-
__author__ = 'xinghang'

import  sys
reload(sys)
sys.setdefaultencoding('utf8')
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import Request
import traceback
from demo.pipelines.stat import *


class oneSipder(Spider):

    name = 'douyu_m'
    download_delay = 0.5
    allowed_domains = ["douyu.com"]

    def start_requests(self):
        for one in range(318624, 318625):
                url = 'https://m.douyu.com/%s' % one
                yield Request(
                    url,
                    headers={ 'User-Agent': 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7A341 Safari/528.16' },
                    callback=self.parse_item
                )


    def parse_item(self, response):

        print '*****************************************************'
        print response
        print '*****************************************************'
        staturltotal()
        sel = Selector(response)

        try:
            video_url= sel.xpath('.//*[@id="dy-video-player"]/@src')
            print ''
            print video_url
            print ''

        except Exception,e:
            print traceback.print_exc()
