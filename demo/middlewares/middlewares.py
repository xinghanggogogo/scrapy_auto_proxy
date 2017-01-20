# -*- coding: utf-8 -*-

import random
import base64
import tornado
import json
import tornado.httpclient
import tornado.ioloop
from demo.models.proxymodel import *
from demo.settings import PROXIES
from demo.utils import proxy_utils
import traceback

class RandomUserAgent(object):

    def __init__(self, agents):
        self.agents = agents

    # 通过crawler方法获得setting配置
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('USER_AGENTS'))

    def process_request(self, request, spider):
        random_UA = random.choice(self.agents)
        request.headers.setdefault('User-Agent', random_UA.setdefault('User_Agetndxinghang'))
        print "**********User-Agent:"+random_UA


class ProxyMiddleware(object):

    def __init__(self):
        self.utils = proxy_utils

    # 通过import方法获得setting配置,配置proxy
    def process_request(self, request, spider):
        proxy = random.choice(PROXIES)

        if proxy['user_pass']:
            request.meta['proxy'] = "http://%s" % proxy['ip_port']
            encoded_user_pass = base64.encodestring(proxy['user_pass'])
            request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
            print "**********Proxy need password:" + proxy['ip_port']

        else:
            print "**********Proxy dont need password:" + proxy['ip_port']
            request.meta['proxy'] = "http://%s" % proxy['ip_port']

    # 动态抓取proxy自动配置
    # def process_request(self, request, spider):
    #     proxies = proxymodel.select()
    #     proxy = random.choice(proxies)
    #     while (not self.utils.test_valid(proxy)):
    #         #删除无效代理
    #         try:
    #             unvalid_proxy = proxymodel.get(proxymodel.id == proxy.id)
    #             unvalid_proxy.delete_instance()
    #             print '成功删除。'
    #         except:
    #             print traceback.print_exc()
    #             print '删除失败。'
    #         proxy = random.choice(proxies)
    #
    #     request.meta['proxy'] = "http://%s" % (proxy.ip + ':' + proxy.port)
    #     print "**********Proxy dont need password:"+ '' +proxy.ip + ':' + proxy.port



