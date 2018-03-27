
# -*- coding: utf-8 -*-

"""
@author: cap_ljf
@time: 18-3-19 下午3:37
"""
import json
import re

import time
from scrapy_redis.spiders import RedisSpider

from NewsCommentsSpider.items import CommentItem


class News163Spider(RedisSpider):
    name = 'news163'
    redis_key = 'news163_url'

    '''
        新闻链接：http://news.163.com/18/0327/09/DDT69BST0001875O.html
        评论链接：http://comment.news.163.com/news2_bbs/DD8EK3DC000189FH
        评论接口：http://comment.news.163.com/api/v1/products/a2869674571f77b5a0867c3d71db5856/threads/DD8EK3DC000189FH/comments/newList?offset=0&limit=40
    '''
    def __init__(self):
        self.allowed_domains = ['www.news.163.com']
        self.url = 'http://comment.news.163.com/news2_bbs/'

    def parse(self, response):
        text = str(response.body, encoding='utf-8')
        content = re.match(r'getData\(\n(.*)\)', text).group(1)
        content = json.loads(content)
        comments = content['comments']
        id = re.match(r'.*threads/(.*)/comments/.*', response.url).group(1)
        url = self.url + id
        for i in comments:
            comment = comments[i]
            item = CommentItem()
            item['url'] = url
            item['comment'] = comment['content']
            print(comment['user'])
            item['author'] = comment['user']['nickname'][:49] # 由于网易用户昵称可能超过50个字符,太长的话就截取前50个字符
            item['praise'] = comment['vote']
            item['create_time'] = self.getTimeStamp(comment['createTime'])
            yield item

    def getTimeStamp(self, t):
        timeArray = time.strptime(t, "%Y-%m-%d %H:%M:%S")
        timestamp = time.mktime(timeArray)
        return timestamp