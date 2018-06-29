# coding=utf-8

import requests
import traceback


class HtmlDownloader(object):
    def download(self, url):
        if url is None:
            return None

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        'Accept': 'application / json, text / javascript, * / *; q = 0.01',
        'Accept - Encoding': 'gzip, deflate, br',
        'Accept - Language': 'zh - CN, zh;q = 0.9',
        'Connection': 'keep - alive',
        }

        response = requests.get(url, headers=headers)
        try:
            if response.status_code == 200:
                response.encoding = 'utf-8'
                return response.text
        except:
            traceback.print_exc()

