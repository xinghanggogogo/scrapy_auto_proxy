# -*- coding: utf-8 -*-

import traceback
import datetime
import hashlib
import json
import codecs

from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals

from demo.models.namemodel import *
from demo.models.ebookmodel import *
from demo.models.proxymodel import *
from demo.models.bookmetamodel import *
from demo.models.bookcommentmodel import *
from demo.models.tvshowmodel import *
from demo.models.onemodel import *

from demo.items.nameItem import *
from demo.items.ebookItem import *
from demo.items.proxyItem import *
from demo.items.bookmetaItem import *
from demo.items.tvshowItem import *
from demo.items.oneItem import *

from demo.pipelines.stat import *

class DemoPipeline(object):

    def __init__(self):
        self.duplicates = {}
        dispatcher.connect(self.spider_closed, signals.spider_closed)

        # 文件
        # self.proxy_file = codecs.open('proxy.json', 'w', encoding='utf-8')
        self.name_file = codecs.open('name.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):

        # 爬取代理信息
        if isinstance(item, proxyItem):
            try:
                model = proxymodel()
                content = ''
                for k, v in item.iteritems():
                    setattr(model, k, v)
                    if v is not None:
                        try:
                            if k == 'ip':
                                content += v
                            if k == 'port':
                                content += v
                        except Exception,e:
                            print "key:", k, "value:", v
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

        # 将one上的图片信息存入数据库
        if isinstance(item, oneItem):
            try:
                model = onemodel()
                content = ''
                for k, v in item.iteritems():
                    setattr(model, k, v)
                    if v is not None:
                        try:
                            if k == 'img_url':
                               content += v
                            if k == 'img_author':
                               content += v
                        except Exception,e:
                            print "key:", k, "value:", v
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

        # 将英文名字信息存入数据库：
        # if isinstance(item, nameItem):
        #     try:
        #         model = namemodel()
        #         content = ''
        #         for k, v in item.iteritems():
        #             setattr(model, k, v)
        #             if v is not None:
        #                 try:
        #                     if k == 'ename':
        #                        content += v
        #                     if k == 'gender':
        #                        content += v
        #                 except Exception,e:
        #                     print "key:", k, "value:", v
        #                     print traceback.print_exc()
        #             else:
        #                 content += ""
        #
        #         model.md5 = hashlib.md5(content).hexdigest()
        #         model.create_time = datetime.datetime.now()
        #         model.update_time = datetime.datetime.now()
        #         model.flag = 0
        #         model.product = None
        #
        #         model.save()
        #         statsuccessitem()
        #     except Exception, e:
        #         print traceback.print_exc()
        #
        #         statfailitem()
        #         pass

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
                    # 用isbn10和isbn13生成md5做唯一性标示
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

        if isinstance(item, bookmetaItem):
            try:
                model = bookmetaModel()
                content = ''
                for k, v in item.iteritems():
                    setattr(model, k, v)
                    # 用isbn10和isbn13生成md5做唯一性标示
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

        if isinstance(item, bookcommentItem):
            try:
                model = bookcommentModel()
                content = ''
                for k, v in item.iteritems():
                    setattr(model, k, v)
                    #用isbn10和isbn13生成md5做唯一性标示
                    if v is not None:
                        try:
                            if k == 'title':
                                content += v
                        except Exception, e:
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

        if isinstance(item, tvshowItem):
            try:
                model = tvshowModel()
                content = ''
                for k, v in item.iteritems():
                    setattr(model, k, v)

                    if v is not None:
                        try:
                            if k == 'anchor':
                                content += v
                            if k == 'source':
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

        print ''
        print '----------spider "%s" finish at %s----------' % (spider.name, datetime.datetime.now())
        print 'total_url: ' + str(geturltotal()),'total_parse_item: ' + str(getitemtotal())
        print 'load_item_success: ' + str(getsuccessitem()) + '  ' + 'load_item_fail: ' + str(getfailitem())
        print 'sync: ' + str(getsyncitem())
        print ''
