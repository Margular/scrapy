# -*- coding: utf-8 -*-
import scrapy
from picture.items import PictureItem

class ChunmeimeiSpider(scrapy.Spider):
    name = "chunmeimei"
    allowed_domains = ["symmz.com"]
    start_urls = (
        'http://www.symmz.com/',
    )

    custom_settings = {
        'FILES_STORE' : '/media/cui/5AE823D1E823A9E9/图片/chunmeimei'
    }

    def parse(self, response):
        for url in response.xpath("//a[@class='tag-font-size-14']/@href").extract()[1:]:
            url = response.urljoin(url)
            yield scrapy.Request(url , self.parse1)

    def parse1(self , response):
        for url in response.css("div.colum > div > div > div > div > a::attr('href')").extract():
            url = response.urljoin(url)
            yield scrapy.Request(url , self.parse2)
        next_url = response.xpath("//a[text()='下一页']/@href").extract()
        if next_url:
            next_url = response.urljoin(next_url[0])
            yield scrapy.Request(next_url , self.parse1)

    def parse2(self , response):
        item = PictureItem()
        item['file_urls'] = response.xpath("//img[@id='maxImg1']/@src").extract()
        yield item
        next_url = response.xpath("//a[text()='下一页']/@href").extract()
        if next_url:
            next_url = response.urljoin(next_url[0])
            yield scrapy.Request(next_url , self.parse2)
