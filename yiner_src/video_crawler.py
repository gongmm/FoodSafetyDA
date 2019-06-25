'''
作者：艾小张 
来源：CSDN 
原文：https://blog.csdn.net/sinat_26549677/article/details/84548471 
'''


import re
import os,shutil
import requests,threading
import json
from urllib.request import urlretrieve
from pyquery import PyQuery as pq
from multiprocessing import Pool

dir_name = 'cctv_video'

class cctv_spider():
    def __init__(self):
        # 设置User Agent模拟浏览器访问
        self.header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Safari/605.1.15',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'Cache-Control': 'max-age=0',
        'Proxy-Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'}
        self.url = 'https://search.cctv.com/ifsearch.php?page=1&qtext=食品&sort=relevance&pageSize=20&type=video&vtime=-1&datepid=5&channel=不限&pageflag=0&qtext_str=食品'
        self.totalpage = 0
        # 设置多线程数量
        self.thread_num = 32
        # 设置视频信息列表字典
        self.video_dict = {}
        # ts文件列表
        self.ts_lists = []
        # 当前已经下载的文件数目
        #self.i = 0
        # 调用网页获取
        json_data = self.get_json_page(self.url)
        if json_data:
            # 解析网页
            self.parse_json(json_data)

    def get_json_page(self, url):
        try:
            print('正在请求目标网页....\n',url)
            response=requests.get(url, headers=self.header, verify=False)
            if response.status_code==200:
                #print(response.text)
                print('请求目标网页完成....\n 准备解析....')
                #self.header['referer'] = url
                return response.text
        except Exception as err:
            print(err)
            print('请求目标网页失败，请检查错误重试！')
            return None

    def parse_json(self, json_data):
        print('目标信息正在解析........')
        text = json.loads(json_data)
        print(type(text))
        if text and 'totalpage' in text.keys():
            self.totalpage = text.get('totalpage')
        if text and 'list' in text.keys():
            item_list = text.get('list')
            # 仅获得标题和url，可排除重复标题项
            # 剔除CCTV-10科教频道的视频
            for item in item_list:
                if item.get('channel') == 'CCTV-10科教频道':
                    continue
                title = item.get('all_title')
                title = title.split(']')[-1]
                self.video_dict[title] = item.get('urllink')
        print(self.video_dict)
        print('解析完成，获取视频列表')
        self.get_m3u8()

    def get_m3u8(self):
        '''
        for key in self.video_dict:
            html = self.get_json_page(self.video_dict.get(key))
            if html:
                # 获取videoCenterId
                doc = pq(html)
                script = doc('.nr_1 script:first').text()
                pattern = re.compile('guid_Ad_VideoCode = "\w*"')
                result = re.search(pattern, script)
                if result: 
                    videoCenterId = result.group()
                    #print ('videoCenterId raw ' + videoCenterId)
                    videoCenterId = videoCenterId.split('"')[-2]
                    print ('videoCenterId ' + videoCenterId)

                    self.m3u8_url = 'http://asp.cntv.kcdnvip.com/asp/hls/1200/0303000a/3/default/' + videoCenterId + '/1200.m3u8'
                    try:
                        response = requests.get(self.m3u8_url, headers=self.header)
                        html = response.text
                        print('获取m3u8文件成功，准备下载文件')
                        self.title = key
                        self.parse_ts(html)
                    except Exception as err:
                        print(err)
                        print('缓存文件请求错误，请检查错误')
        '''
        key = '国务院食品安全办 多数居民存在食品安全认知误区'
        html = self.get_json_page(self.video_dict.get(key))
        if html:
            # 获取videoCenterId
            doc = pq(html)
            script = doc('.nr_1 script:first').text()
            pattern = re.compile('guid_Ad_VideoCode = "\w*"')
            result = re.search(pattern, script)
            if result: 
                videoCenterId = result.group()
                #print ('videoCenterId raw ' + videoCenterId)
                videoCenterId = videoCenterId.split('"')[-2]
                print ('videoCenterId ' + videoCenterId)

                self.m3u8_url = 'http://asp.cntv.kcdnvip.com/asp/hls/1200/0303000a/3/default/' + videoCenterId + '/1200.m3u8'
                try:
                    response = requests.get(self.m3u8_url, headers=self.header)
                    html = response.text
                    print('获取m3u8文件成功，准备下载文件')
                    self.title = ''.join(key.split()) # 去掉字符串中间的空格
                    self.parse_ts(html)
                except Exception as err:
                    print(err)
                    print('缓存文件请求错误，请检查错误')

    def parse_ts(self, html):
        pattern = re.compile('\d+.ts')
        self.ts_lists = re.findall(pattern, html)
        print(self.ts_lists)
        print('信息提取完成......\n准备下载...')
        self.pool()

    def pool(self):
        print('经计算需要下载%d个文件' % len(self.ts_lists))
        self.ts_url = self.m3u8_url[:-10]
        if self.title not in os.listdir():
            os.makedirs(self.title)
        print('正在下载...所需时间较长，请耐心等待..')
        #开启多进程下载
        i = 0
        pool=Pool(16) # 加锁初始化
        pool.map(self.save_ts, [ts_list for ts_list in self.ts_lists])
        pool.close()
        pool.join()
        print('下载完成')
        self.ts_to_mp4()

    def sort_key(self, s):
        if s:
            try:
                c = re.findall('\d+', s)[0]
            except:
                c = -1
            return int(c)

    def ts_to_mp4(self):
        print('ts文件正在进行转录mp4......')
        if dir_name not in os.listdir():
            os.makedirs(dir_name)
        dir_list = os.listdir(self.title)
        if '.DS_Store' in dir_list:
            index = dir_list.index('.DS_Store')
            dir_list.pop(index)
        dir_list.sort(key=self.sort_key)
        for index, file in enumerate(dir_list):
            file = os.path.join(self.title, file)
            dir_list[index] = file
        dirs = '|'.join(dir_list) 
        dirs = 'concat:' + dirs
        str = 'ffmpeg -y -i "' + dirs + '" -vn -acodec copy ' + dir_name + '/' + self.title + '.wav'
        os.system(str)
        filename = self.title + '.wav'
        if os.path.isfile(filename):
            print('转换完成')
            shutil.rmtree(self.title)
        

    def save_ts(self, ts_list):
        try:
            ts_urls = self.ts_url + '/{}'.format(ts_list)
            print(ts_urls)
            #urlretrieve(url=ts_urls, 
            #    filename=self.title + '/{}'.format(ts_list))
        except Exception as err:
            print(err)
            print('保存文件出现错误')


if __name__ == '__main__':
    cctv_spider()
