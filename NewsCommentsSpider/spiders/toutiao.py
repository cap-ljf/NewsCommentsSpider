# -*- coding: utf-8 -*-

"""
@author: cap_ljf
@time: 18-3-16 上午11:25
"""
import json
import re

from scrapy_redis.spiders import RedisSpider

from NewsCommentsSpider.items import CommentItem


class ToutiaoSpider(RedisSpider):
    name = 'toutiao'
    redis_key = 'toutiao_url'

    '''
        新闻链接：https://www.toutiao.com/a6533396129860551182/
        评论接口：https://www.toutiao.com/api/comment/list/?group_id=6533396129860551182&item_id=6533396129860551182
    '''
    def __init__(self):
        self.allowed_domains = ['www.toutiao.com']
        self.url = 'https://www.toutiao.com/a'

    def parse(self, response):
        content = json.loads(response.body.decode())
        id = re.search(r'([0-9]+)', response.url).group(1)
        url = self.url + str(id)
        comments = content['data']['comments']
        for comment in comments:
            item = CommentItem()
            item['url'] = url
            item['comment'] = comment['text']
            item['author'] = comment['user']['name']
            item['praise'] = comment['digg_count']
            item['create_time'] = comment['create_time']
            yield item

