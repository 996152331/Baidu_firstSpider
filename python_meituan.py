#coding=utf-8
'''
1.需要两个美团账号

2.需要用抓包工具抓到红包的url

3.思路：红包会显示第x个是大红包，一个账号打开红包做轮询检测，当满足下个是大红包的条件时，用另一个账号抢
'''

import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from lxml import etree
'''使用抓包工具,抓手机的请求包'''
'''使selenium加载已保存的cookie来访问网页'''
'''修改请求头为手机端'''
chrome_options = webdriver.ChromeOptions()
profile_dir = r"F:\Google\Chrome\User Data"
chrome_options.add_argument("user-data-dir=" + os.path.abspath(profile_dir))
chrome_options.add_argument(
    'user-agent="Mozilla/5.0 (Linux; Android 8.0; ONEPLUS A3010 Build/OPR1.170623.032; wv) AppleWebKit/537.36 (KHTML\
    , like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044112 Mobile Safari/537.36 MicroMessenger/6.6\
    .7.1320(0x26060739) NetType/WIFI Language/zh_CN"')
driver = webdriver.Chrome(r'F:\Google\Chrome\Application\chromedriver.exe', chrome_options=chrome_options)
refresh_num = 1


def get_url(url, number):
    '''
    :param url: 红包url
    :param number: 第几个是大红包
    :return:
    '''
    driver.get(url)
    driver.maximize_window()
    get_receive_number(number)


def get_receive_number(number):
    '''
    获取已抢个数
    :param number: 第几个是大红包
    :return:
    '''
    global refresh_num
    driver.refresh()
    time.sleep(3)
    response = driver.page_source
    response = etree.HTML(response)
    num = response.xpath('//*[@class="comment_ul"]/li')
    print('已被抢 %s个 ' % int(len(num)-1))
    if len(num) > number-1:
        print(len(num), number-1)
        driver.quit()
        print('最大红包已被抢')
    elif len(num) == number-1:
        driver.quit()
        print('快抢~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    else:
        print('正在等待大红包出现的时机')
        refresh_num += 1
        print('已刷新%s次' % refresh_num)
        print('=========================')
        get_receive_number(number)


if __name__ == '__main__':
    url = 'https://activity.waimai.meituan.com/coupon/sharechannelredirect/B2EA8E1ABA8B47EA82DB475BA17B517D?urlKey=7FAF\
    84C9DD5F427DAC95CBBE1D93A174'
    get_url(url, 9)     # 红包界面显示的第几个是大红包
