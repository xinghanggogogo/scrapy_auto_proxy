# -*- coding: utf-8 -*-

import traceback
import datetime
import hashlib

from demo.models.namemodel import *
from demo.models.ebookmodel import *
from demo.items.nameItem import *
from demo.items.ebookItem import *
from demo.pipelines.stat import *
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals

class DemoPipeline(object):

    def __init__(self):
        self.duplicates = {}
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def process_item(self, item, spider):

        if isinstance(item, nameItem):
            try:
                model = namemodel()
                content = ''
                for k, v in item.iteritems():
                    setattr(model, k, v)
                    if v is not None:
                        try:
                            if k == 'ename':
                               content += v
                            if k == 'gender':
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
        ret = str(datetime.datetime.now()) + ' ' + spider.name + '  ' + \
              'scrapy_urltotal:' + str(geturltotal()) + '  ' + 'parse_itemtoal:' + str(getitemtotal()) + ' ' + \
              'savedb_success:' + str(getsuccessitem()) + ' ' + 'savedb_fail:' + str(getfailitem()) + ' ' + 'sync:' + str(
            getsyncitem()) + '\r\n'
        print ret