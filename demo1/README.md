# 第一个Demo
### 1. 新建目录
新建一个新的工作目录，如：G:\PythonNotes

### 2. 初始化项目
在当前（G:\PythonNotes）目录下使用cmd终端运行指令：
```
scrapy startproject demo1
```
该命令将会创建包含下列内容的 demo1 目录:
```
demo1/
    scrapy.cfg
    demo1/
        __init__.py
        items.py
        pipelines.py
        settings.py
        spiders/
            __init__.py
            ...
```
这些文件分别是:
- scrapy.cfg: 项目的配置文件
- demo1/: 该项目的python模块。之后您将在此加入代码。
- demo1/items.py: 项目中的item文件.
- demo1/pipelines.py: 项目中的pipelines文件.
- demo1/settings.py: 项目的设置文件.
- demo1/spiders/: 放置spider代码的目录.

### 3. 编写第一个爬虫(Spider)
> Spider是用户编写用于从单个网站(或者一些网站)爬取数据的类。
>
> 其包含了一个用于下载的初始URL，如何跟进网页中的链接以及如何分析页面中的内容， 提取生成 item 的方法。
>
> 为了创建一个Spider，您必须继承 scrapy.Spider 类， 且定义以下三个属性:
>
> - name: 用于区别Spider。 该名字必须是唯一的，您不可以为不同的Spider设定相同的名字。
> - start_urls: 包含了Spider在启动时进行爬取的url列表。 因此，第一个被获取到的页面将是其中之一。 后续的URL则从初始的URL获取到的数据中提取。
> - parse() 是spider的一个方法。 被调用时，每个初始URL完成下载后生成的 Response 对象将会作为唯一的参数传递给该函数。 该方法负责解析返回的数据(response data)，提取数据(生成item)以及生成需要进一步处理的URL的 Request 对象。

在demo1/spiders 目录下新建 demo1_spider.py
> 例子来源： https://zhuanlan.zhihu.com/p/24669128
```
import scrapy

class Demo1Spider(scrapy.spiders.Spider):
    name = 'demo1'
    start_urls = ['http://woodenrobot.me']

    def parse(self, response):
        # 利用xPath解析文章标题(下文解释)
        titles = response.xpath('//a[@class="post-title-link"]/text()').extract()
        for title in titles:
            # 打印
            print(title.strip())

```

### 4. Selectors选择器简介
> 从网页中提取数据有很多方法。Scrapy使用了一种基于 XPath 和 CSS 表达式机制: Scrapy Selectors 。 关于selector和其他提取机制的信息请参考 Selector文档 。
> 
> 这里给出XPath表达式的例子及对应的含义:
> 
> - /html/head/title: 选择HTML文档中 <head> 标签内的 <title> 元素
> - /html/head/title/text(): 选择上面提到的 <title> 元素的文字
> - //td: 选择所有的 <td> 元素
> - //div[@class="mine"]: 选择所有具有 class="mine" 属性的 div 元素
> XPath详细教程: http://www.w3school.com.cn/xpath/index.asp


上面的例子中，我们访问http://woodenrobot.me后，利用浏览器开发者工具（F12）查看页面元素，可以发现标题部分的样式如：
```
<a class="post-title-link" href="/2018/02/09/使用-Git-拉取远程仓库分支到本地分支/" itemprop="url">使用 Git 拉取远程仓库分支到本地分支</a>
```
所以就有了我们例子中xPath的写法：
```
response.xpath('//a[@class="post-title-link"]/text()').extract() //获取样式为post-title-link的<a>标签中的文本内容
```


### 5. 启动
打开终端进入项目根目录（G:\PythonNotes\Demo1）运行下列命令：
```
scrapy crawl woodenrobot
```
