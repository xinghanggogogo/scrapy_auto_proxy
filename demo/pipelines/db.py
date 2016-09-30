# -*- coding: utf-8 -*-

import traceback
import datetime
import hashlib
import json
import codecs

from demo.models.namemodel import *
from demo.models.ebookmodel import *
from demo.items.nameItem import *
from demo.items.ebookItem import *
from demo.items.proxyItem import *
from demo.pipelines.stat import *
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals

class DemoPipeline(object):

    def __init__(self):
        self.duplicates = {}
        dispatcher.connect(self.spider_closed, signals.spider_closed)

        #文件信息
        self.proxy_file = codecs.open('proxy.json', 'w', encoding='utf-8')
        self.name_file = codecs.open('name.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):

    #将英文名字信息存入数据库：
    #     if isinstance(item, nameItem):
    #         try:
    #             model = namemodel()
    #             content = ''
    #             for k, v in item.iteritems():
    #                 setattr(model, k, v)
    #                 if v is not None:
    #                     try:
    #                         if k == 'ename':
    #                            content += v
    #                         if k == 'gender':
    #                            content += v
    #                     except Exception,e:
    #                         print "key:",k,"value:",v
    #                         print traceback.print_exc()
    #                 else:
    #                     content += ""
    #
    #             model.md5 = hashlib.md5(content).hexdigest()
    #             model.create_time = datetime.datetime.now()
    #             model.update_time = datetime.datetime.now()
    #             model.flag = 0
    #             model.product = None
    #
    #             model.save()
    #             statsuccessitem()
    #         except Exception, e:
    #             print traceback.print_exc()
    #
    #             statfailitem()
    #             pass

        #爬取代理信息，写入json文件
        if isinstance(item, proxyItem):

            try:
                line = json.dumps(dict(item), ensure_ascii=False) + "\n"
                self.proxy_file.write(line)
                statsuccessitem()

            except Exception, e:
                print traceback.print_exc()
                statfailitem()
                pass

        # 将英文名字信息写入json文件
        if isinstance(item, nameItem):

            try:
                line = json.dumps(dict(item), ensure_ascii=False) + "\n"
                self.name_file.write(line)
                statsuccessitem()

            except Exception, e:
                print traceback.print_exc()
                statfailitem()
                pass

        if isinstance(item, ebookItem):
            try:
                model = ebookModel()
                content = ''
                for k, v in item.iteritems():
                    setattr(model, k, v)
                    #用isbn10和isbn13生成md5做唯一性标示
                    if v is not None:
                        try:
                            if k == 'isbn10':
                                content += v
                            if k == 'isbn13':
                                content += v
                        except Exception,e:
                            print "key:",k,"value:",v
                            print traceback.print_exc()
                    else:
                        content += ""

                model.md5 = hashlib.md5(content).hexdigest()
                model.create_time = datetime.datetime.now()
                model.update_time = datetime.datetime.now()
                model.flag = 0
                model.product = None

                model.save()
                statsuccessitem()

            except Exception, e:
                print traceback.print_exc()
                statfailitem()
                pass

    def spider_closed(self, spider):

        self.file.close()

        print ''
        print '----------scrapy finish----------'
        print 'time: ' + str(datetime.datetime.now())
        print 'spider: ' + spider.name
        print 'total_url: ' + str(geturltotal())
        print 'total_parse_item: ' + str(getitemtotal())
        print 'load_item_success: ' + str(getsuccessitem()) + '  ' + 'load_item_fail: ' + str(getfailitem())
        print 'sync: ' + str(getsyncitem())
        print ''
