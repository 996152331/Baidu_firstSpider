# coding=utf-8

from DataOutput import DataOutput
from HtmlDownloader import HtmlDownloader
from HtmlParser import HtmlParser
from URLManager import UrlManager
import traceback


class SpiderMan(object):
    def __init__(self):
        self.manager = UrlManager()
        self.downloader = HtmlDownloader()
        self.parser = HtmlParser()
        self.output = DataOutput()

    def crawl(self, root_url):
        # 添加入口url
        self.manager.add_new_url(root_url)
        # 判断url管理器中是否有线的url,同时判断抓取了多少个url
        while self.manager.has_new_url() and self.manager.old_url_size() < 5:
            try:
                # 从url管理器获取新的url
                new_url = self.manager.get_new_url()
                # html下载器下载网页
                html = self.downloader.download(new_url)
                # html解析器抽取网页数据
                new_urls, data = self.parser.parser(new_url, html)
                # 将抽取的url添加到url管理器中
                self.manager.add_new_urls(new_urls)
                # 数据存储器存储文件
                self.output.store_data(data)
                print('已经抓取%s个链接 %s' % (self.manager.old_url_size(), data['title']))
            except Exception as e:
                traceback.print_exc()
            # 数据存储器将文件输出成指定格式
        self.output.output_html()


if __name__ == '__main__':
    spider_man = SpiderMan()
    url = 'http://baike.baidu.com/view/284853.html'
    spider_man.crawl(url)