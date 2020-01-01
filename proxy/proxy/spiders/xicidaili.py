# -*- coding: utf-8 -*-

import scrapy
from proxy.items import ProxyItem


class XicidailiSpider(scrapy.Spider):
    name = "xicidaili"
    allowed_domains = ["xicidaili.com"]
    start_urls = ['http://www.xicidaili.com/nn',
                  'http://www.xicidaili.com/nt',
                  'http://www.xicidaili.com/wn',
                  'http://www.xicidaili.com/wt']

    max_page = 10

    def parse(self, response):
        item = ProxyItem()

        temp = response.xpath('//table[@id="ip_list"]/tr[position()>1]')

        for index in range(len(temp)):
            item["ip"] = temp[index].xpath('td[position()=2]/text()').extract()
            item["port"] = temp[index].xpath('td[position()=3]/text()').extract()
            item["protocol"] = temp[index].xpath('td[position()=6]/text()').extract()
            item["country"] = temp[index].xpath('td[position()=1]/img/@alt').extract()
            item["address"] = temp[index].xpath('td[position()=4]/a/text() | td[position()=4]/text()').extract()
            for address in item["address"]:
                if address.strip():
                    item["address"] = [address]
            item["anonymous"] = temp[index].xpath('td[position()=5]/text()').extract()
            item["speed"] = temp[index].xpath('td[position()=7]/div/@title').extract()
            item["ctime"] = temp[index].xpath('td[position()=8]/div/@title').extract()
            item["ttl"] = temp[index].xpath('td[position()=9]/text()').extract()
            item["vdate"] = temp[index].xpath('td[position()=10]/text()').extract()

            for i in item:  # strip blank
                item[i] = item[i][0].strip() if item[i] else ""

            yield item

        next_url = response.urljoin(response.xpath('//a[@class="next_page"]/@href').extract()[0])
        if int(next_url.split('/')[-1]) <= self.max_page:
            yield scrapy.Request(next_url, self.parse)
