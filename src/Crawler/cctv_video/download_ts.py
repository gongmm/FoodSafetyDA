import re
import os, shutil
import requests, threading
import json
from urllib.request import urlretrieve
from pyquery import PyQuery as pq
from multiprocessing import Pool
import random
import time
import csv
from functools import partial
import numpy as np

UA_LIST = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]

base_dir = 'ts_videos'
dir_name = 'wav_audios'
des_dir = 'csv'
csv_name = 'cctv_videos.csv'
# 设置User Agent模拟浏览器访问
header = {
    'User-Agent': random.choice(UA_LIST),
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'Cache-Control': 'max-age=0',
    'Proxy-Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}


def get_page(url):
    try:
        print('正在请求目标网页....\n', url)
        response = requests.get(url, headers=header, verify=False, timeout=10)
        if response.status_code == 200:
            print('请求目标网页完成....\n 准备解析....')
            return response.text
    except Exception as err:
        print(err)
        print('请求目标网页失败，请检查错误重试！')
        return None


def get_m3u8(video_dict):
    # 所有视频文件都下载
    for key in video_dict:
        video_dir = key
        file_path = os.path.join(base_dir, video_dir)
        if base_dir not in os.listdir():
            os.makedirs(base_dir)
        print(video_dir)
        if video_dir not in os.listdir(base_dir):
            if '?' in video_dir:
                video_dir = video_dir.replace('?', '？')
                file_path = file_path.replace('?', '？')
            if video_dir not in os.listdir(base_dir):
                os.makedirs(file_path)
        elif '0.ts' in os.listdir(file_path):
            print('已下载ts文件')
            ts_to_wav(file_path)
            return

        times = 1
        while True:
            # 得到m3u8地址
            html = get_page(video_dict[key])
            if html and not pq(html)('body').text() =='':
                # 获取videoCenterId
                doc = pq(html)
                script = doc('.nr_1 script:first').text()
                pattern = re.compile('guid_Ad_VideoCode = "\w*"')
                result = re.search(pattern, script)
                if not result:
                    script = doc('.nr_1 script:nth-child(8)').text()
                    pattern = re.compile('"videoCenterId","\w*"')
                    result = re.search(pattern, script)

                if result:
                    videoCenterId = result.group()
                    videoCenterId = videoCenterId.split('"')[-2]
                    print('videoCenterId ' + videoCenterId)

                    m3u8_url = 'http://asp.cntv.kcdnvip.com/asp/hls/1200/0303000a/3/default/' + videoCenterId + '/1200.m3u8'

                    try:
                        response = requests.get(m3u8_url, headers=header)
                        html = response.text
                        print('获取m3u8文件成功，准备下载文件')
                        parse_ts(file_path, html, m3u8_url)
                        break
                    except Exception as err:
                        print(err)
                        print('缓存文件请求错误，请检查错误')
                        if not os.listdir(file_path):
                            shutil.rmtree(file_path)
                else:
                    print('无法获取videoCenterId！')
                    if os.listdir(file_path):
                        shutil.rmtree(file_path)
                    print('————无法爬取%s的视频————' % key)
                    break
            else:
                print('无法获取视频网页内容！')

                times += 1
                if times >= 5:
                    if os.listdir(file_path):
                        shutil.rmtree(file_path)
                    print('————无法爬取%s的视频————' % key)
                    break

                print('正在重新获取网页内容...\n')




def parse_ts(file_path, html, m3u8_url):
    pattern = re.compile('\d+.ts')
    ts_lists = re.findall(pattern, html)
    print(ts_lists)
    print('信息提取完成......\n准备下载...')
    pool(file_path, m3u8_url, ts_lists)
    ts_to_wav(file_path)


def pool(file_path, m3u8_url, ts_lists):
    print('经计算需要下载%d个文件' % len(ts_lists))
    ts_url = m3u8_url[:-10]
    if base_dir not in os.listdir():
        os.makedirs(base_dir)
    video_dir = os.path.split(file_path)[-1]
    print(video_dir)
    if video_dir not in os.listdir(base_dir):
        os.makedirs(file_path)
    elif '0.ts' in os.listdir(file_path):
        print('已下载ts文件')
        return

    print('正在下载...所需时间较长，请耐心等待..')
    # 开启多进程下载
    i = 0
    pool = Pool(16)
    func = partial(save_ts, ts_url=ts_url, file_path=file_path)
    pool.map(func, [ts_list for ts_list in ts_lists])
    pool.close()
    pool.join()
    print('下载完成')


def sort_key(s):
    if s:
        try:
            c = re.findall('\d+', s)[0]
        except:
            c = -1
        return int(c)


def ts_to_wav(file_path):
    # 检测是否已存在wav文件
    video_dir = os.path.split(file_path)[-1]
    filename = os.path.join(dir_name, video_dir + '.wav')
    if dir_name not in os.listdir():
        os.makedirs(dir_name)
    elif os.path.isfile(filename):
        print('wav文件已存在')
        return

    # 开始格式转换
    print('ts文件正在进行转录wav......')
    dir_list = os.listdir(file_path)
    if '.DS_Store' in dir_list:
        index = dir_list.index('.DS_Store')
        dir_list.pop(index)
    dir_list.sort(key=sort_key)
    for index, file in enumerate(dir_list):
        file = os.path.join(file_path, file)
        dir_list[index] = file
    dirs = '|'.join(dir_list)
    dirs = 'concat:' + dirs
    # wav的格式必须是pcm_s16le
    str = 'ffmpeg -loglevel quiet -y -i "' + dirs + '" -vn -acodec pcm_s16le -f wav -ar 16000 ' + filename
    os.system(str)

    print(filename)
    if os.path.isfile(filename):
        print('转换完成')
        # shutil.rmtree(self.title)


def save_ts(ts_list, ts_url, file_path):
    try:
        ts_urls = ts_url + '/{}'.format(ts_list)
        print(ts_urls)
        urlretrieve(url=ts_urls,
                    filename=file_path + '/{}'.format(ts_list))
        time.sleep(1)
    except Exception as err:
        print(err)
        print('保存文件出现错误')


def download_ts():
    video_dict = dict()
    path = os.path.join(des_dir, csv_name)
    ts_dir_list = os.listdir(base_dir)
    ts_dir_arr = np.array(ts_dir_list)

    with open(path, 'r', encoding='gbk') as f:
        r = csv.DictReader(f)
        for row in r:
            title = ''.join(row['title'].split())  # 去掉字符串中间的空格
            if not ((title == ts_dir_arr).any()):
                video_dict[title] = row['video_url']

    get_m3u8(video_dict)


if __name__ == '__main__':
    download_ts()
