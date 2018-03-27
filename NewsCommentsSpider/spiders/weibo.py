# -*- coding: utf-8 -*-

"""
@author: cap_ljf
@time: 18-3-16 上午11:25
"""
import json
import re

import time
from scrapy_redis.spiders import RedisSpider

from NewsCommentsSpider.items import CommentItem


class WeiboSpider(RedisSpider):
    name = 'weibo'
    redis_key = 'weibo_url'

    '''
        微博原文链接：'https://m.weibo.cn/status/' + 单条微博id
        最热评论接口：'https://m.weibo.cn/single/rcList?format=cards&id=' + 单条微博id + '&type=comment&hot=1&page=' + 页码
        最新评论接口：'https://m.weibo.cn/api/comments/show?id=' + 单条微博id + '&page=' + 页码
    '''
    def __init__(self):
        self.allowed_domains = ['www.weibo.cn']
        self.url = 'https://m.weibo.cn/status/'

    def parse(self, response):
        content = json.loads(response.body.decode())
        if self.isHot(response.url):
            '''热评'''
            comments = content[1]['card_group']
        else:
            '''  '''
            comments = content['data']['data']

        id = re.match(r'.*?([0-9]+)', response.url).group(1)
        url = self.url+id
        for comment in comments:
            item = CommentItem()
            item['url'] = url
            item['comment'] = comment['text']
            item['author'] = comment['user']['screen_name']
            item['praise'] = comment['like_counts']
            # format time
            item['create_time'] = self.formatTime(comment['created_at'])
            yield item

    def isHot(self, url):
        status = re.match(r'single', url)
        if status is not None:
            return True
        else:
            return False

    def formatTime(self, t):
        if len(t)<10:
            t = '2018-'+t+' 12:00'
        t = t + ":00"
        timeArray = time.strptime(t, "%Y-%m-%d %H:%M:%S")
        timestamp = time.mktime(timeArray)
        return timestamp

