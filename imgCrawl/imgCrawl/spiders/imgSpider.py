# -*- coding: utf-8 -*-
import scrapy

from imgCrawl.items import ImgcrawlItem

from urllib.parse import urljoin
from scrapy.http import Request


class ImgspiderSpider(scrapy.Spider):
    name = 'imgSpider'
    # allowed_domains = ['841ff.com/']
    start_urls = ['http://841ff.com//']
    # 伪装浏览器
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36',
    }

    # 获取板块，所有的图片板块
    def parse(self, response):
        file_name = response.xpath(
            '//div[@class="wrap nav"]/ul[1]/li/a/text()').extract()
        all_urls = response.xpath(
            '//div[@class="wrap nav"]/ul[1]/li/a/@href').extract()
        for i in range(len(file_name)):
            print((str(i + 1) + ':' + file_name[i]), end=" ")
        print()
        val = input("请输入编号(别不看键盘打英文，中文，就识别数字):")
        print()
        num = input("下载页数(别不看键盘打英文，中文，就识别数字):")
        # 将指定页面生成完整的网址
        url = urljoin(response.url, all_urls[int(val) - 1])
        # 将请求送的二级页面处理中
        yield Request(url, callback=self.parse_img,
                      headers=self.headers)
        # 获取10页
        for i in range(1, int(num)):
            page_urls = response.xapth(
                '//div[@ class="pagination"]/a["' + str(i) + '"]/@href')
            page_urls = "http://841ff.com" + page_urls
            # 跳转函数
            yield Request(page_urls, callback=self.parse_img)

    # 获取所有的
    def parse_img(self, response):
        item = ImgcrawlItem()
        for i in range(5, 21):
            file_name = response.xpath(
                '//div[@class="box list channel"]/ul/li[' + str(
                    i) + ']/a/text()').extract()
            file_name = str(file_name).strip('[]')
            cur_url = response.xpath(
                '//div[@class="box list channel"]/ul/li[' + str(
                    i) + ']/a/@href').extract()
            for j in cur_url:
                url = "http://841ff.com" + j
                yield Request(url, callback=self.parse_img_img,
                              meta={'file_name': file_name})

    # 图片
    def parse_img_img(self, response):
        item = ImgcrawlItem()
        for i in response.xpath('//img/@src').extract():
            item['img_url'] = [i]
            item['img_title'] = str(response.meta['file_name']).strip()
            # print(item['img_url'])
            # print(item['img_title'])
            yield item
