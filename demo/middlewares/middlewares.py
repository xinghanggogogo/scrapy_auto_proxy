import random
import base64

from demo.settings import PROXIES

class RandomUserAgent(object):

    def __init__(self, agents):
        self.agents = agents

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('USER_AGENTS'))

    def process_request(self, request, spider):
        random_UA = random.choice(self.agents)
        request.headers.setdefault('User-Agent', random_UA)
        print "**********User-Agent:"+random_UA


class ProxyMiddleware(object):

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