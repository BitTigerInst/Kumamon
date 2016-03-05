# coding=utf-8
__author__ = 'jing'


from scrapy.spider import BaseSpider
from scrapy.http import Request
from qiubai.items import QiubaiItem

# uncomment below to fix issue of "Scrapy gives URLError: <urlopen error timed out>"
from scrapy import optional_features
optional_features.remove('boto')


class QuibaiSpider(BaseSpider):
    name = "qiubai"

    start_urls = [
        "http://www.qiushibaike.com"
    ]

    #-------------------------------
    # mission1: 提取所有笑话和作者名字
    #-------------------------------
    # def parse(self, response):
    #     for ele in response.xpath('//div[@class="article block untagged mb15"]'):
    #         authors = ele.xpath('./div[@class="author clearfix"]/a[2]/h2/text()').extract()
    #         contents = ele.xpath('./div[@class="content"]/text()').extract()
    #         yield QiubaiItem(author=authors, content=contents)


    #-------------------------------
    # mission2: 提取所有笑话的所有评论和评论者名字!
    #-------------------------------
    def parse(self, response):
        for href in response.xpath('//span[@class="stats-comments"]/a/@href').extract():  # extract()是提取成列表格式
            detail_url = response.urljoin(href) # 创建详情网页地址[基础域名+详情网页增量地址]
            req = Request(detail_url, self.parse_detail_page)  # 这里通过Request类创建一个实例req,即从主页发送一个到下级详情网页的请求
                                                               # 然后又会返回一个response,通过参数二来处理这个response, 参数一提供想要请求的下级网页的地址
            item = QiubaiItem()
            req.meta["item"] = item # 这里需要得到上下两级网页的内容, 所以需要把Item传给下级!
            yield req # 实际调用这个req

    def parse_detail_page(self, response): # 回调函数, 和上面parse()的参数是一模一样的,功能和mission1中的parse()一模一样
        """
        注意:由于这里采用了yield的缘故,所以这里函数只处理一个笑话
        :param response:
        :return:
        """
        ### 取出上级已经创建好的item
        item = response.meta["item"]

        ### 提取作者和笑话
        authors = response.xpath('//div[@class="author clearfix"]/a[2]/h2/text()').extract()
        contents = response.xpath('//div[@class="content"]/text()').extract()

        # 某些网页的某些元素可能为空, 即会返回一个空的list,那么你去空list里面slice/dice就会出错! 所以需要先判断list是否为空
        item["authors"] = authors[0] if authors else ""
        item["contents"] = contents[0] if contents else ""

        ### 提取评论和评论者
        comments = []
        # # method1:找评论文字部分的最小父级
        # for comment in response.xpath('//div[@class="replay"]'):
        #     comment_author = comment.xpath('./a/text()').extract()[0]
        #     comment_content = comment.xpath('./span/text()').extract()[0]

        # method2: 上层父级属性的值符合一定规律
        for comment in response.xpath('//div[starts-with(@class, "comment-block clearfix floor")]'):  # start后面有s,是dash不是under_score
            comment_author = comment.xpath('./div[2]/a/text()').extract()[0]  # extract()返回的是list,但是这里是每个comment只有一个评论者和一个评论,所以要提取第一个元素
            comment_content = comment.xpath('./div[2]/span/text()').extract()[0]
            comments.append({'comment_author': comment_author, 'comment_content': comment_content}) # 构建成一个dict,然后赋值给item用

        item["comments"] = comments

        ### 返回提取信息
        yield item


