#coding=utf-8
#环境2.7
#通过观察网络请求network-all-p_6/ 发现是通过网址控制ajax加载的,用列表推导即可
#个别几个商品是宣传广告,获取不到价格,导致最后结果名称和价格错位
import sys,os
reload(sys)
sys.setdefaultencoding('utf-8')
import requests
from lxml import etree

#xlsx
from openpyxl import Workbook
wb = Workbook()
sheet = wb.active

headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.9',
'Cache-Control': 'max-age=0',
'Connection': 'keep-alive',
'Cookie': 'PHPSESSID=kgid2o25g6doghh7h67jbrisu7; user_region_id=think%3A%7B%22parent_id%22%3A%222%22%2C%22region_id%22%3A%22382%22%7D; think_language=zh-CN; Hm_lvt_8eee4cacb173e36099ceadd434aa2376=1527848941,1528091210; idss=cc; Hm_lpvt_8eee4cacb173e36099ceadd434aa2376=1528091581; amvid=4d01e0bee7360de2a428375988a81041',
'Host': 'www.meidebi.com',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}

aline = 0
bline = 0
def get_url(url):
	try:
		response = requests.get(url,headers=headers)
		response = response.text.encode('utf-8')
		selector = etree.HTML(response)
		titles = selector.xpath('//ul[@class="clearfix"]/li/a[1]/div[2]/text()')
		moneys = selector.xpath('//ul[@class="clearfix"]/li/a[1]/div[3]/span/i/text()')
		global aline, bline
	
		#save
		for title, money in zip(titles, moneys):
			sheet["A%d" % (aline+1)].value = title
			sheet["B%d" % (bline+1)].value = money
			aline = aline+1
			bline = bline+1
		wb.save('info.xlsx')
		print(url,'Finsh!')
	except:
		pass


if __name__ == '__main__':
	url_list = ['http://www.meidebi.com/index_n/p_{}/'.format(str(i)) for i in range(1,11)]
	for url in url_list:
		get_url(url)
