# -*- coding: utf-8 -*-

BOT_NAME = 'NewsCommentsSpider'

SPIDER_MODULES = ['NewsCommentsSpider.spiders']
NEWSPIDER_MODULE = 'NewsCommentsSpider.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

DOWNLOADER_MIDDLEWARES = {
    'NewsCommentsSpider.middlewares.UserAgentMiddleware': 400,
    'NewsCommentsSpider.middlewares.CookiesMiddleware': 401,
    'NewsCommentsSpider.middlewares.HeadersMiddleware': 402,
    'NewsCommentsSpider.middlewares.ProxiesMiddleware': 403,
}

ITEM_PIPELINES = {
    'NewsCommentsSpider.pipelines.MySQLPipeline': 300,
}

DEFAULT_ITEM_CLASS = 'NewsCommentsSpider.pipelines.MySQLPipeline'

DOWNLOAD_DELAY = 2  # 每个下载请求之间间隔两秒


# redis配置
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
SCHEDULER_PERSIST = True
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
REDIS_HOST = 'localhost'
REDIS_PORT = '6379'
REDIS_DB = 0
REDIS_PASSWD = ''

# mysql配置
MYSQL_HOST = 'localhost'
MYSQL_DBNAME = 'minsheng'
MYSQL_USER = 'root'
MYSQL_PASSWD = 'xjj520520ljf'
