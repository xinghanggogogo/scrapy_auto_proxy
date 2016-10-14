#coding:utf8

import tornado.httpclient
import tornado.ioloop
import json

from demo.models.proxymodel import *

def handle_request(response, proxy):
        if response.error:
            print "This proxy is not valid", response.error
            test_count()

        else:
            print 'Thanks God,this proxy is valid.'
            return True

def test_valid(proxy):

    ip = proxy.ip
    port = proxy.port

    tornado.httpclient.AsyncHTTPClient.configure("tornado.curl_httpclient.CurlAsyncHTTPClient")
    http_client = tornado.httpclient.AsyncHTTPClient()

    request = tornado.httpclient.HTTPRequest(url="http://shikanon.com/", proxy_host=ip, proxy_port=port, connect_timeout=4)
    is_valid = http_client.fetch(request, callback=handle_request)
    tornado.ioloop.IOLoop.instance().start()

    return is_valid

def test_count():

    proxy_count = proxymodel.select().count()
    if proxy_count <20:
        #再次爬取怎么写..
        pass
