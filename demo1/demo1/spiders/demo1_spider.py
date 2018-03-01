import scrapy

class Demo1Spider(scrapy.spiders.Spider):
    name = 'demo1'
    start_urls = ['http://woodenrobot.me']

    def parse(self, response):
        # 利用xPath解析文章标题
        titles = response.xpath('//a[@class="post-title-link"]/text()').extract()
        for title in titles:
            # 打印
            print(title.strip())
