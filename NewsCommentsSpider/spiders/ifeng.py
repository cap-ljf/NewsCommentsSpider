# -*- coding: utf-8 -*-

"""
@author: cap_ljf
@time: 18-3-27 上午8:59
"""
import json
import re
import time
import urllib.parse

from scrapy_redis.spiders import RedisSpider

from NewsCommentsSpider.items import CommentItem


class IfengSpider(RedisSpider):
    name = "ifeng"
    redis_key = "ifeng_url"

    '''
        新闻链接：http://news.ifeng.com/a/20180326/57059350_0.shtml
        评论链接：http://gentie.ifeng.com/view.html?docUrl=http%3A%2F%2Fnews.ifeng.com%2Fa%2F20180326%2F57059350_0.shtml
        评论接口：http://comment.ifeng.com/get.php?docUrl=http%3A%2F%2Fnews.ifeng.com%2Fa%2F20180326%2F57075847_0.shtml&job=1&p=1&pageSize=50
    '''
    def __init__(self):
        self.allowed_domains = ['www.ifeng.com']
        self.url = "http://news.ifeng.com/a/"

    def parse(self, response):
        content = json.loads(response.body.decode())
        encoded_url = re.match(r'http://comm.*?docUrl=(http.*?shtml).*',response.url).group(1)
        decoded_url = urllib.parse.unquote(encoded_url)
        comments = content['comments']
        for comment in comments:
            item = CommentItem()
            item['url'] = decoded_url
            item['comment'] = comment['comment_contents']
            item['author'] = comment['uname']
            item['praise'] = comment['uptimes']
            item['create_time'] = float(comment['create_time'])
            yield item


    def formatTime(self, t):
        t = t+":00"
        timeArray = time.strptime(t, "%Y-%m-%d %H:%M:%S")
        timestamp = time.mktime(timeArray)
        return timestamp

