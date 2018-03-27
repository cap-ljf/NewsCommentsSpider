# -*- coding: utf-8 -*-
import logging

import pymysql
from datetime import datetime

from NewsCommentsSpider.settings import *


class MySQLPipeline(object):
    # 定义数据存储方式
    def __init__(self):
        try:
            self.connect = pymysql.connect(
                host=MYSQL_HOST,
                db=MYSQL_DBNAME,
                user=MYSQL_USER,
                passwd=MYSQL_PASSWD,
                charset='utf8',
                use_unicode=True
            )
            # 通过cursor执行增删改查
            self.cursor = self.connect.cursor()
            logging.debug('mysql conn success!')
        except Exception as error:
            logging.error('mysql conn error!:', error)

    def process_item(self, item, spider):
        try:
            self.cursor.execute(
                """insert into comment(url, comment, author, praise, create_time)
                                  value (%s, %s, %s, %s, %s)""",
                (item['url'],
                 item['comment'],
                 item['author'],
                 item['praise'],
                 datetime.fromtimestamp(item['create_time'])
                 )
            )
            # 提交sql语句
            self.connect.commit()
        except Exception as error:
            # 异常打印日志
            logging.error("数据库插入异常:", error)

        return item

    def __del__(self):
        try:
            # if self.cursor:
            #     self.cursor.close()
            if self.connect:
                self.connect.close()
        except Exception as error:
            logging.error("conn or cursor 关闭失败:", error)
