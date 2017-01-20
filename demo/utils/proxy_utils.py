#coding:utf8

import tornado.httpclient
import tornado.ioloop
import json
import urllib2
import time
import traceback

from tornado import web, gen
from demo.models.proxymodel import *

def handle_request(response):
    if response.error:
        print "This proxy is not valid"
        print response.error
        print response
        # test_count()
        return False

    else:
        print 'Thanks God,this proxy is valid.'
        return True

def test_valid(proxy):

    ip = proxy.ip
    port = proxy.port

    cookies = urllib2.HTTPCookieProcessor()
    proxyHandler = urllib2.ProxyHandler({"http": r'http://%s:%s' % (ip, port)})
    opener = urllib2.build_opener(cookies, proxyHandler)
    opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36')]
    t1 = time.time()

    try:
        print '&&&&&&&&&&'
        res = opener.open('http://www.baidu.com', timeout=10)
        print '++++++++++'
        print res.code
        print '++++++++++'
        timeused = time.time() - t1
        if res.code == 200:
            print '*****'
            print ip + ':' + port + '用时：' + str(timeused) +'s'
            print '*****'
            return True
        else:
            print '*****Proxy 不可用*****'
            return False

    except Exception, e:
        print traceback.print_exc()
        return False

