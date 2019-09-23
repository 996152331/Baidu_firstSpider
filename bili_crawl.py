import requests
from fake_useragent import UserAgent
import time
import os

ua = UserAgent()

headers = {
    'User-Agent': ua.ie
}


def requests_man():
    '''
    获取视频链接
    :return:
    '''
    content = 0
    # https://vc.bilibili.com/p/eden/rank#/?tab=%E5%85%A8%E9%83%A8
    url = 'https://api.vc.bilibili.com/board/v1/ranking/top?page_size=5&next_offset=&tag=%E4%BB%8A%E6%97%A5%E7%83%AD%E9%97%A8&platform=pc'
    response = requests.get(url, headers=headers).json()
    items = response['data']['items']

    for item in items:
        video_playurl = item['item']['video_playurl']
        video_name = item['item']['description']
        # print(video_name)
        # print(video_playurl)
        video_name = 'Bilibili_' + str(content) + '.mp4'
        download(video_playurl, r'C:\Users\Fu\Desktop\file\%s' % video_name)
        # download(video_playurl, r'C:\Users\Administrator\Desktop\file\%s' % video_name)
        print(video_name)
        content += 1
        print('[已完成{}个]'.format(content))
        # adb_push(video_name)


def download(video_playurl, download_path):
    '''
    下载视频
    :param video_playurl: 链接地址
    :param download_path: 下载地址
    :return:
    '''
    size = 0
    start = time.time()
    response = requests.get(video_playurl, headers=headers, stream=True)
    chunk_size = 3024
    content_size = int(response.headers['content-length'])  # 1
    if response.status_code == 200:
        print('[文件大小]: %0.2f MB' % (content_size / chunk_size / 1024))
        with open(download_path, 'wb') as f:
            for data in response.iter_content(chunk_size=chunk_size):
                f.write(data)
                size += len(data)
                # 进度条
                print('\r' + '[下载的进度]:%s %.2f %%' % (
                    '>' * int(size * 50 / content_size), float(size / content_size * 100)), end='')

    end = time.time()
    print('\n' + '视频下载完成, 用时{}s'.format(end - start))


def adb_push(video_name):
    '''
    push到手机,遇到bug,没实时刷新，app检测不到视频，手动拖动实时刷新，
    :param video_name:视频名
    :return:
    '''

    print('video_name : %s' % video_name)
    os.chdir(r'C:\Users\Administrator\Desktop\file')
    os.system('adb push %s /sdcard/video' % video_name)


if __name__ == '__main__':
    requests_man()
    # appium发布时，发现手机无法实时监测到push过来的视频，尝试android虚拟机，发现app对虚拟机做        
    # 了检测
    # 未做功能：发布成功后把,原视频名加入到txt中，发布前先检查txt中是否有原视频名，去重
     
