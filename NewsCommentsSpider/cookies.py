# -*- coding: utf-8 -*-

"""
@author: cap_ljf
@time: 18-3-16 下午9:32
"""

# encoding=utf-8

import base64
import json
from imp import reload

import requests
# import sys
import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import logging
# from yumdama import identify
#
# reload(sys)
# sys.setdefaultencoding('utf8')
IDENTIFY = 1  # 验证码输入方式:        1:看截图aa.png，手动输入     2:云打码
COOKIE_GETWAY = 2  # 0 代表从https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18) 获取cookie   # 1 代表从https://weibo.cn/login/获取Cookie  # 2 代表用chromedriver从https://weibo.cn/login/获取cookie
dcap = dict(DesiredCapabilities.PHANTOMJS)  # PhantomJS需要使用老版手机的user-agent，不然验证码会无法通过
dcap["phantomjs.page.settings.userAgent"] = (
    "Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; Nexus S Build/GRK39F) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"
)
logger = logging.getLogger(__name__)
logging.getLogger("selenium").setLevel(logging.WARNING)  # 将selenium的日志级别设成WARNING，太烦人

"""
输入你的微博账号和密码，可去淘宝买。
建议买几十个，微博限制的严，太频繁了会出现302转移。
或者你也可以把时间间隔调大点。
"""
myWeiBo = [
    {'no': 'tianbi1462447@163.com', 'psw': 'ou29bxhqdc'},
    # {'no': 'gaofangrr922814@163.com', 'psw': 'dwimdxiqdp'},
    # {'no': 'soufens4123@163.com', 'psw': 'ewzfdxnqes'},
    # {'no': 'caitao8556835@163.com', 'psw': '0wiqouimvg'},
    # {'no': 'nuecheng03992592@163.com', 'psw': 'bjn20w92bx'},
    # {'no': 'baodiaom103@163.com', 'psw': '0ximdu29bw'},
    # {'no': 'zeiduidw733385@163.com', 'psw': 'xxnqd8nqd8'},
    # {'no': 'bozhenht50824@163.com', 'psw': '0xzruunqu8'},
    # {'no': 'kamanci93634@163.com', 'psw': 'uwib0yxsuc'},
    # {'no': 'heimp6905283@163.com', 'psw': 'uunqbnlwvc'},
    # {'no': 'huancanpw491434@163.com', 'psw': 'u8n9bx49bj'},
    # {'no': 'zhoukouf388@163.com', 'psw': 'xx9moybmoy'},
    # {'no': 'shibaokj4055413@163.com', 'psw': 'ew9q0ximuw'},
    # {'no': 'chubol932950@163.com', 'psw': '0w9f0xzwvc'},
    # {'no': 'pifanls1575@163.com', 'psw': 'eu2x0yxwes'},
    # {'no': 'zhaioq0893912@163.com', 'psw': 'xx99uyzadg'},
    # {'no': 'wenzi904453@163.com', 'psw': 'ownqxxzxdg'},
    # {'no': 'guizaothn531223@163.com', 'psw': 'dpnqxximou'},
    # {'no': 'huxiang92409@163.com', 'psw': 'u8n7uyiqds'}
]


def getCookie(account, password):
    if COOKIE_GETWAY == 0:
        return get_cookie_from_login_sina_com_cn(account, password)
    elif COOKIE_GETWAY == 1:
        return get_cookie_from_weibo_cn(account, password)
    elif COOKIE_GETWAY == 2:
        return get_cookie_by_selenium_chrome(account,password)
    else:
        logger.error("COOKIE_GETWAY Error!")


def get_cookie_from_login_sina_com_cn(account, password):
    """ 获取一个账号的Cookie """
    loginURL = "https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)"
    username = base64.b64encode(account.encode("utf-8")).decode("utf-8")
    postData = {
        "entry": "sso",
        "gateway": "1",
        "from": "null",
        "savestate": "30",
        "useticket": "0",
        "pagerefer": "",
        "vsnf": "1",
        "su": username,
        "service": "sso",
        "sp": password,
        "sr": "1440*900",
        "encoding": "UTF-8",
        "cdult": "3",
        "domain": "sina.com.cn",
        "prelt": "0",
        "returntype": "TEXT",
    }
    session = requests.Session()
    r = session.post(loginURL, data=postData)
    jsonStr = r.content.decode("gbk")
    info = json.loads(jsonStr)
    if info["retcode"] == "0":
        logger.warning("Get Cookie Success!( Account:%s )" % account)
        cookie = session.cookies.get_dict()
        # return json.dumps(cookie)
        return cookie
    else:
        logger.warning("Failed!( Reason:%s )" % info["reason"])
        return ""


# def get_cookie_from_weibo_cn(account, password):
#     """ 获取一个账号的Cookie """
#     try:
#         browser = webdriver.PhantomJS(desired_capabilities=dcap)
#         browser.get("https://weibo.cn/login/")
#         time.sleep(2)
#
#         failure = 0
#         print(browser.title)
#         while "微博" in browser.title and failure < 5:
#             failure += 1
#             browser.save_screenshot("aa.png")
#             username = browser.find_element_by_id("loginName")
#             username.clear()
#             username.send_keys(account)
#
#             psd = browser.find_element_by_xpath('//input[@type="password"]')
#             psd.clear()
#             psd.send_keys(password)
#             try:
#                 code = browser.find_element_by_name("code")
#                 code.clear()
#                 if IDENTIFY == 1:
#                     code_txt = input("请查看路径下新生成的aa.png，然后输入验证码:")  # 手动输入验证码
#                 else:
#                     from PIL import Image
#                     img = browser.find_element_by_xpath('//form[@method="post"]/div/img[@alt="请打开图片显示"]')
#                     x = img.location["x"]
#                     y = img.location["y"]
#                     im = Image.open("aa.png")
#                     im.crop((x, y, 100 + x, y + 22)).save("ab.png")  # 剪切出验证码
#                     code_txt = identify()  # 验证码打码平台识别
#                 code.send_keys(code_txt)
#             except Exception as e:
#                 pass
#
#             commit = browser.find_element_by_name("submit")
#             commit.click()
#             time.sleep(3)
#             if "我的首页" not in browser.title:
#                 time.sleep(4)
#             if '未激活微博' in browser.page_source:
#                 print('账号未开通微博')
#                 return {}
#
#         cookie = {}
#         if "我的首页" in browser.title:
#             for elem in browser.get_cookies():
#                 cookie[elem["name"]] = elem["value"]
#             logger.warning("Get Cookie Success!( Account:%s )" % account)
#         return cookie
#     except Exception as e:
#         logger.warning("Failed %s!" % account)
#         return ""
#     finally:
#         try:
#             browser.quit()
#         except Exception as e:
#             pass

'''
因为从get_cookie_from_login_sina_com_cn函数获得的cookie无效,
get_cookie_from_weibo_cn函数PhantomJS可能引版本问题一直异常，此方法获取有效的cookie
'''
def get_cookie_by_selenium_chrome(account, password):
    browser = webdriver.Chrome()
    browser.get('https://weibo.cn/login/')
    time.sleep(2)
    username = browser.find_element_by_id("loginName")
    username.clear()
    username.send_keys(account)
    psw = browser.find_element_by_id("loginPassword")
    psw.clear()
    psw.send_keys(password)
    commit = browser.find_element_by_id("loginAction")
    commit.click()
    time.sleep(1)
    try:
        cookie = {}
        if "我的首页" in browser.title:
            for elem in browser.get_cookies():
                cookie[elem["name"]] = elem["value"]
        return cookie
    except Exception as e:
        logger.warning("Failed %s!" % account)
        return ""
    finally:
        try:
            browser.quit()
        except Exception as e:
            pass


def getCookies(weibo):
    """ 获取Cookies """
    cookies = []
    for elem in weibo:
        account = elem['no']
        password = elem['psw']
        cookie = getCookie(account, password)
        if cookie != None:
            cookies.append(cookie)

    return cookies


# cookies = getCookies(myWeiBo)
# logger.warning("Get Cookies Finish!( Num:%d)" % len(cookies))
#
