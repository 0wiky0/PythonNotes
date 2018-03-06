from scrapy import cmdline

cmdline.execute("scrapy crawl doubanTop -o douban.json".split())
