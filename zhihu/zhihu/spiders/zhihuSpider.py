# coding=utf-8
import scrapy

from zhihu.settings import USERNAME, PASSWORD

# uncomment below to fix issue of "Scrapy gives URLError: <urlopen error timed out>"
from scrapy import optional_features

optional_features.remove('boto')


class ZhihuSpider(scrapy.Spider):
    name = "zhihu"

    start_urls = ["http://www.zhihu.com/#signin"]

    def parse(self, response): # 第一个请求
        return scrapy.FormRequest.from_response(
            response,
            formdata={'email': USERNAME, 'password': PASSWORD},
            callback=self.after_login,
            method="POST",
            url="http://www.zhihu.com/login/email"
        )

    def after_login(self, response): # 第二个请求
        #print response.body  #不知道返回的是什么,先打印看看
        return scrapy.Request("https://www.zhihu.com", self.parse_index)

    def parse_index(self, response): # 第三个请求
        #print response.body
        for item in response.xpath('//a[@class="question_link"]/text()').extract():
            print item



