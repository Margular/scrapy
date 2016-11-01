import random
import logging

class RandomUserAgent(object):
    def __init__(self , agents):
        self.agents = agents

    @classmethod
    def from_crawler(cls , crawler):
        return cls(crawler.settings.getlist('USER_AGENTS'))

    def process_request(self , request , spider):
        request.headers.setdefault('User-Agent' , random.choice(self.agents))

class RandomProxy(object):
    def __init__(self):
        with open('proxy.json' , 'r') as f:
            self.proxies = eval(f.read())

    def process_request(self , request , spider):
        proxy = random.choice(self.proxies)
        spider.logger.info('Switch proxy: %s' % str(proxy))
        request.meta['proxy'] = '%s://%s:%s' % (proxy['protocol'].lower() , proxy['ip'] , proxy['port'])
