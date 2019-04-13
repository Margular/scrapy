import json
import random
import logging

class RandomUserAgent(object):
    def __init__(self, agents):
        self.agents = agents

    @classmethod
    def from_crawler(cls, crawler):
        return cls(open(crawler.settings.get('USER_AGENT_FILE')).read().split('\n'))

    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', random.choice(self.agents))

class RandomProxy(object):
    def __init__(self):
        self.proxies = json.load(open('../proxy/proxy.json'))

    def process_request(self, request, spider):
        proxy = random.choice(self.proxies)
        spider.logger.info('Switch proxy: ' + repr(proxy))
        request.meta['proxy'] = '%s://%s:%s' % (proxy['protocol'].lower() , proxy['ip'] , proxy['port'])
