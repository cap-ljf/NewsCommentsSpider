# -*- coding: utf-8 -*-

"""
@author: cap_ljf
@time: 18-3-16 下午9:56
"""
from scrapy import cmdline

if __name__ == '__main__':
    cmdline.execute("scrapy crawl news163".split())
