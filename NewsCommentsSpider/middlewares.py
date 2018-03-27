# -*- coding: utf-8 -*-
import random

from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware

# from NewsCommentsSpider.cookies import cookies
from NewsCommentsSpider.user_agent import agents


class UserAgentMiddleware(UserAgentMiddleware):
    """ 换User-Agent """
    pass
    def process_request(self, request, spider):
        agent = random.choice(agents)
        request.headers['User-Agent'] = agent


class CookiesMiddleware(object):
    """ 四个网站，选择相应cookie """
    # def process_request(self, request, spider):
    #     if spider.name == 'weibo':
    #         cookie = random.choice(cookies)
    #         request.cookies = cookie

class HeadersMiddleware(object):
    pass


class ProxiesMiddleware(object):
    pass
