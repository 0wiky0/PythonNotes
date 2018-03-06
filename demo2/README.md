# Demo2 -- 爬取豆瓣电影TOP250
### 工具和环境
语言：python 3.6
IDE： Pycharm
浏览器：Chrome
爬虫框架：Scrapy 1.5.0

### 网页详情
网页链接： https://movie.douban.com/top250
列表Item项样式：
```
<div class="item">
    <div class="pic">
        <em class="">1</em>
        <a href="https://movie.douban.com/subject/1292052/">
            <img width="100" alt="肖申克的救赎" src="https://img3.doubanio.com/view/photo/s_ratio_poster/public/p480747492.webp" class="">
        </a>
    </div>
    <div class="info">
        <div class="hd">
            <a href="https://movie.douban.com/subject/1292052/" class="">
                <span class="title">肖申克的救赎</span>
                <span class="title">&nbsp;/&nbsp;The Shawshank Redemption</span>
                <span class="other">&nbsp;/&nbsp;月黑高飞(港)  /  刺激1995(台)</span>
            </a>
            <span class="playable">[可播放]</span>
        </div>
        <div class="bd">
            <p class="">
                导演: 弗兰克·德拉邦特 Frank Darabont&nbsp;&nbsp;&nbsp;主演: 蒂姆·罗宾斯 Tim Robbins /...<br>
                1994&nbsp;/&nbsp;美国&nbsp;/&nbsp;犯罪 剧情
            </p>

            <div class="star">
                    <span class="rating5-t"></span>
                    <span class="rating_num" property="v:average">9.6</span>
                    <span property="v:best" content="10.0"></span>
                    <span>987073人评价</span>
            </div>

            <p class="quote">
                <span class="inq">希望让人自由。</span>
            </p>
        </div>
    </div>
</div>
```

### 1. 初始化项目
按照第一篇的步骤，我们先建个简单的Spider:
```
import scrapy

class DoubanTopSpider(scrapy.spiders.Spider):
    name = 'doubanTop'
    start_urls = ['https://movie.douban.com/top250']

    def parse(self, response):
        # 利用xPath解析电影标题
        titles = response.xpath('.//div[@class="hd"]/a/span[1]/text()').extract()
        for title in titles:
            # 打印
            print(title.strip())

```
>Tip: 从上文网页样式中可以发现，如果我们要抓取电影名称,不能再使用Demo1中的方式：//span[@class="title"]/text()，因为将会有两个地方与这个
>规则匹配，所以我们再优化一下匹配规则，加长路径确保唯一性：
>```
># 获取样式为hd的<div>标签中，<a>标签内的第一个<span>标签的内容
>response.xpath('.//div[@class="hd"]/a/span[1]/text()').extract()
>```


程序运行后会发现什么都没抓到，发现403错误（没有权限访问此站）。不着急，小问题，我们改造一下请求即可：
```
import scrapy
from scrapy import Request

class DoubanTopSpider(scrapy.spiders.Spider):
    name = 'doubanTop'
    # 添加请求头部信息，还是可以利用F12查看网页的请求信息，从而拿到'User-Agent'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
    }

    # 改用start_requests，支持更丰富的功能
    def start_requests(self):
        url = 'https://movie.douban.com/top250'
        yield Request(url, headers=self.headers)


    def parse(self, response):
        # 利用xPath解析文章标题
        titles = response.xpath('.//div[@class="hd"]/a/span[1]/text()').extract()
        for title in titles:
            # 打印
            print(title.strip())
```
 

**看到输出后，接下来思考两个问题：**
- 如果要获取更多电影信息（排名、评分等），怎么将这些数据结构化，或者说怎么用一个对象来存在这些信息？
- 我们发现上面的代码其实只能获取到25条数据，那么要怎么处理翻页的问题？

### 结构化数据（Item）
#### 定义Item
> Item 是保存爬取到的数据的容器；其使用方法和python字典类似， 并且提供了额外保护机制来避免拼写错误导致的未定义字段错误。
>
> 类似在ORM中做的一样，您可以通过创建一个 scrapy.Item 类， 并且定义类型为 scrapy.Field 的类属性来定义一个Item。 (如果不了解ORM, 不用担心，您会发现这个步骤非常简单)

比如我们记录电影的名称、排名、评分、评论数等数据，那么就可以在项目根目录下找到items.py，然后进行编辑：
```
import scrapy

class DoubanMovieItem(scrapy.Item):
    # 排名
    ranking = scrapy.Field()
    # 电影名称
    movie_name = scrapy.Field()
    # 评分
    score = scrapy.Field()
    # 评论人数
    comment_num = scrapy.Field()
    pass
```
#### 使用Item
在我们的doubanTop_spider文件中引用刚刚添加好的Item
```
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
```
运行后可以看到输出:
```
2018-03-06 13:54:43 [scrapy.core.scraper] DEBUG: Scraped from <200 https://movie.douban.com/top250>
{'comment_num': '545146人评价',
 'movie_name': '大话西游之大圣娶亲',
 'ranking': '15',
 'score': '9.2'}
2018-03-06 13:54:43 [scrapy.core.scraper] DEBUG: Scraped from <200 https://movie.douban.com/top250>
{'comment_num': '376022人评价',
 'movie_name': '教父',
 'ranking': '16',
 'score': '9.2'}
...
...
```
> tip： 如果需要保存抓取的数据至本地只需要修改一下运行指令即可，如保存json格式：scrapy crawl doubanTop -o douban.json

### 自动翻页
>  实现自动翻页一般有两种方法：
> 
> - 在页面中找到下一页的地址；
> - 自己根据URL的变化规律构造所有页面地址。
>
> 一般情况下我们使用第一种方法，第二种方法适用于页面的下一页地址为JS加载的情况。

以下介绍第一种方式的做法，详情见代码：
```
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
```
翻页的问题先简单说到这，后续有需要再单独进行详细介绍。