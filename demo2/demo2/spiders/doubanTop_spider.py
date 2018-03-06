import scrapy
from scrapy import Request
# 注意，demo2.items中的demo2为本项目的目录，具体值视各自项目目录名而定
from demo2.items import DoubanMovieItem

class DoubanTopSpider(scrapy.spiders.Spider):
    name = 'doubanTop'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
    }

    def start_requests(self):
        url = 'https://movie.douban.com/top250'
        yield Request(url, headers=self.headers)

    def parse(self, response):
        # 使用Item,并进行对应的解析及赋值

        item = DoubanMovieItem()
        # 先获取整个列表的数据
        movies = response.xpath('//ol[@class="grid_view"]/li')
        for movie in movies:
            # 对每个Item进行解析
            item['ranking'] = movie.xpath(
                './/div[@class="pic"]/em/text()').extract()[0]
            item['movie_name'] = movie.xpath(
                './/div[@class="hd"]/a/span[1]/text()').extract()[0]
            item['score'] = movie.xpath(
                './/div[@class="star"]/span[@class="rating_num"]/text()'
            ).extract()[0]
            item['comment_num'] = movie.xpath(
                './/div[@class="star"]/span[4]/text()').extract()[0]
            yield item

        # 获取'后页'对应的地址链接
        next_url = response.xpath('//span[@class="next"]/a/@href').extract()
        if next_url:
            # 如果存在'后页'，表示后面还有内容，则进行模拟请求
            next_url = 'https://movie.douban.com/top250' + next_url[0]
            yield Request(next_url, headers=self.headers)
