# -*- coding: utf-8 -*-


import scrapy
from scrapy import Field

class CommentItem(scrapy.Item):
    # 文章链接
    url = Field()
    # 评论内容
    comment = Field()
    # 评论者
    author = Field()
    # 点赞数
    praise = Field()
    # 评论时间
    create_time = Field()
