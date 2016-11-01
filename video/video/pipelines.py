# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

class CutParameter(object):
    def process_item(self, item, spider):
        item['file_urls'] = item['file_urls'].split('?')[0]
        return item
