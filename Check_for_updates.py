'''
因项目组需要保持软件为最新版，而网站下载速度又很慢，需要两三个小时，因而写出这个脚本检查网页上是否有最新版，自动下载，挂到Jenkins
'''

from selenium import webdriver
import time
import os
import fire


def Run():
    try:
        global path
        global driver
        global newest_version
        # 使用自带浏览器
        profile_dir = r"C:\Users\Administrator\AppData\Local\Google\Chrome\User Data"
        options = webdriver.ChromeOptions()
        options.add_argument("--user-data-dir=" + profile_dir)

        # 设置下载路径
        prefs = {'profile.default_content_settings.popups': 0,
                 'download.default_directory': download_path}
        options.add_experimental_option('prefs', prefs)
        driver = webdriver.Chrome(r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe",
                                  chrome_options=options)

        driver.maximize_window()
        driver.implicitly_wait(120)
        driver.get("https://account.simplygon.com/#/downloads")
        driver.find_element_by_xpath('//*[@class="text au-target"]').click()
        driver.find_element_by_xpath('//*[@href="#customerportal"]/img').click()
        driver.find_element_by_xpath('//*[@class="download-link"]/a').click()
        time.sleep(1)
        newest_version = driver.find_element_by_xpath('//*[@class="element-narrow"]/a').get_attribute('href')
        print('最新版本：{0}'.format(newest_version))

        # 拼接
        newest_version = newest_version.split('/')[-1]
        path = os.path.join(download_path, newest_version) 
        print('检测路径下是否有最新版本: \n{0}'.format(path))

        if os.path.exists(path):
            print('目录下已有最新版本啦！')
        else:
            print('目录下没有最新版本，开始下载新版本！')
            # SdkDownloads
            driver.find_element_by_xpath('//*[@class="element-narrow"]/a').click()
            Finished()

    except Exception as err:
        print(err)
    finally:
        driver.quit()


def Finished():
    '''
    等待下载完毕
    :return:
    '''
    list_b = ['Downloading.', 'Downloading..', 'Downloading...', 'Downloading....', 'Downloading           ']
    while not os.path.exists(path):
        for i in list_b:
            print('%s\r' % i, end='')
            time.sleep(0.2)
    print('下载完成！ ')


def V(path):
    '''用命令行获取下载路径'''
    '''Command：python sdk_down.py V --path xxx'''
    global download_path
    download_path = path
    return "目标路径：{path}".format(path=path)


if __name__ == '__main__':
    fire.Fire()
    Run()
    
'''
run.bat
python sdk_down.py V --path C:\Users\Administrator\Desktop\sdk_downloads
'''
