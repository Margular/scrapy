# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import re

from scrapy.exceptions import DropItem


class CheckPipeline(object):
    def process_item(self, item, spider):
        if not re.fullmatch(r'([1-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-4])\.' +
                            r'([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.' +
                            r'([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.' +
                            r'([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])',
                            item['ip']):  # check valid ip address
            raise DropItem('Invalid ip address')

        if int(item['port']) < 1 or int(item['port']) > 65535:  # check valid port
            raise DropItem('Invalid port number')

        if item['protocol'].upper() not in ('HTTP', 'HTTPS', 'SOCKS', 'SOCKS5'):  # check valid protocol
            raise DropItem('Invalid or not known protocol')

        return item


class DuplicatesPipeline(object):
    def __init__(self):
        self.proxies_seen = set()

    def process_item(self, item, spider):
        if item['ip'] + ':' + item['port'] in self.proxies_seen:
            raise DropItem('Duplicate item found')
        else:
            self.proxies_seen.add(item['ip'] + ':' + item['port'])
            return item


class FilterPipeline(object):
    def process_item(self, item, spider):
        # speed < 0.1
        speed = float(re.search(r'[0-9]+(\.[0-9]+)?', item['speed']).group())
        if not speed < 0.1:
            raise DropItem('Low speed item')
        # ctime < 0.1
        ctime = float(re.search(r'[0-9]+(\.[0-9]+)?', item['ctime']).group())
        if not ctime < 0.1:
            raise DropItem('Low ctime item')
        # filter chinese ip
        if item['country'].upper() == 'CN':
            raise DropItem('Chinese ip found')
        # http protocol
        if not item['protocol'].upper() == 'HTTP':
            raise DropItem('Non-HTTP proxy found')

        return item
