import scrapy

class DmozSpider(scrapy.spiders.Spider):
    name = "baidu"
    allowed_domains = ["baidu.com"]
    start_urls = [
        "http://www.baidu.com"
    ]

    def parse(self, response):
        filename = response.url.split("/")[-2]
        with open(filename, 'wb') as f:
            f.write(response.body)