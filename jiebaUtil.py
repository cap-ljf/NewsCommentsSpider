# -*- coding: utf-8 -*-

"""
@author: cap_ljf
@time: 18-4-17 上午8:51
"""
import json
import logging
from collections import Counter

import jieba
import pymysql
from jieba import analyse

jieba.add_word("扎克伯格")


def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
    return stopwords


def get_words(txt):
    seg_list = jieba.cut(txt)
    a = jieba.analyse.extract_tags(txt, topK=30, allowPOS=('a', 'an', 'n', 'nr', 'nt', ''))
    c = Counter()
    for x in seg_list:
        if len(x) > 1 and x != '\r\n' and x in a:
            c[x] += 1
    comments = {}
    i = 0
    for (k, v) in c.most_common(20):
        # if k not in stopwords:
        comments[k] = v
    j = json.dumps(comments, ensure_ascii=False)
    print(comments)


def get_comments():
    try:
        connect = pymysql.connect(
            host="localhost",
            db="minsheng",
            user="root",
            passwd="",
            charset='utf8',
            use_unicode=True
        )
        # 通过cursor执行增删改查
        cursor = connect.cursor()
        logging.debug('mysql conn success!')
    except Exception as error:
        logging.error('mysql conn error!:', error)
    cursor.execute("select comment from comment")
    comments = cursor.fetchall()
    connect.commit()
    if connect:
        connect.close()
    return comments.__str__()


if __name__ == '__main__':
    txt = get_comments()
    get_words(txt)
