# coding=utf-8
import re
import urllib.parse
from lxml import etree


class HtmlParser(object):
    def parser(self, page_url, html_cont):
        '''
        解析页面内容,抽取url和数据
        :param page_url: 下载页面url
        :param html_cont: 下载页面内容
        :return: 返回url和数据
        '''
        if page_url is None or html_cont is None:
            return
        soup = etree.HTML(html_cont)
        new_urls = self._get_new_urls(page_url, soup)
        new_data = self._get_new_data(page_url, soup)
        return new_urls, new_data

    def _get_new_urls(self, page_url, soup):
        '''
        抽取新的url集合
        :param page_url: 下载页面的url
        :param soup: soup
        :return: 返回新的url集合
        '''
        new_urls = set()
        # 抽取符合要求的a标记
        links = soup.xpath('//*[@class="para"]/a/@href')
        for link in links:
            # 拼接成完整的网站
            new_full_url = urllib.parse.urljoin(page_url, link)
            new_urls.add(new_full_url)
        return new_urls

    def _get_new_data(self, page_url, soup):
        '''
        抽取有效数据
        :param page_url: 下载页面的url
        :param soup: soup
        :return: 返回有效数据
        '''
        data = {'url': page_url}
        title = soup.xpath('//*[@class="lemmaWgt-lemmaTitle-title"]/h1/text()')
        data['title'] = title
        summary = soup.xpath('//*[@class="lemma-summary"]//text()')
        # 获取tag中包含的所有文本内容,包括子孙tag中的内容,并将结果作为unicode字符串返回
        data['summary'] = summary
        return data
