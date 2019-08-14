import re
import os,shutil
import requests,threading
import json
from urllib.request import urlretrieve
from pyquery import PyQuery as pq
from multiprocessing import Pool
import random
import time
import csv

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
# working_path = '/Users/yiner/Desktop/lab-exp/FoodSafetyDA/yiner_src'
# working_path = 'D:/FoodSafetyDA/yiner_src'
page_url_head = 'https://search.cctv.com/ifsearch.php?page='
page_url_tail = '&qtext=食品&sort=relevance&pageSize=20&type=video&vtime=-1&datepid=1&channel=不限&pageflag=0&qtext_str=食品'

des_dir = 'csv'
csv_name = 'cctv_videos.csv'

class cctv_spider():
    def __init__(self):
        # 设置User Agent模拟浏览器访问
        self.header = {
        'User-Agent': random.choice(UA_LIST),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'Cache-Control': 'max-age=0',
        'Proxy-Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
        }
        self.url = page_url_head + str(1) + page_url_tail
        self.totalpage = 0

        # 设置视频信息列表字典
        self.video_dict = {}
        # ts文件列表
        self.ts_lists = []

        # csv文件的行
        self.rows = []

        # 调用网页获取
        json_data = self.get_page(self.url)
        if json_data:
            # 解析网页
            self.parse_json(json_data)
            if not self.totalpage == 0:
                if self.totalpage > 50:  # 50页后为重复内容
                    self.totalpage = 50
                for i in range(1, self.totalpage):
                    print(i)
                    self.url = page_url_head + str(i) + page_url_tail
                    time.sleep(1)
                    json_data = self.get_page(self.url)
                    self.parse_json(json_data)
                    for key, dic in self.video_dict.items():
                        row = []
                        # 按headers的顺序添加
                        row.append(key)
                        row.append(dic.get('uploadtime'))
                        row.append(dic.get('video_url'))
                        print(row)
                        if not len(row) == 0:
                        	self.rows.append(row)
                    self.video_dict = {}

        headers = ['title', 'uploadtime', 'video_url']

        if des_dir not in os.listdir():
            os.mkdir(des_dir)
        path = os.path.join(des_dir, csv_name)
        with open(path, 'w', encoding='utf-8', newline='') as f:
            f_csv = csv.writer(f)
            f_csv.writerow(headers)
            f_csv.writerows(self.rows)
        print('转换成功！')

    def get_page(self, url):
        try:
            print('正在请求目标网页....\n',url)
            response=requests.get(url, headers=self.header, verify=False, timeout=10)
            if response.status_code==200:
                print('请求目标网页完成....\n 准备解析....')
                return response.text
        except Exception as err:
            print(err)
            print('请求目标网页失败，请检查错误重试！')
            return None

    def parse_json(self, json_data):
        print('目标信息正在解析........')
        text = json.loads(json_data)
        #print(type(text))
        if text and 'totalpage' in text.keys():
            if self.totalpage == 0:
                self.totalpage = text.get('totalpage')
        if text and 'list' in text.keys():
            item_list = text.get('list')
            # 仅获得标题和url，可排除重复标题项
            # 剔除CCTV-10科教频道的视频
            for item in item_list:
                if item.get('channel') == 'CCTV-10科教频道':
                    continue
                if item.get('durations') >= 180:
                    continue
                if '2018' not in item.get('uploadtime'):
                    continue
                title = item.get('all_title')
                title = title.split(']')[-1]
                # 信息存入字典
                self.video_dict[title] = {}
                self.video_dict[title]['video_url'] = item.get('urllink')
                self.video_dict[title]['uploadtime'] = item.get('uploadtime')
        print(self.video_dict)
        print('解析完成，获取视频列表')
        self.get_m3u8()

    def get_m3u8(self):
        # 所有视频文件都下载
        for key in self.video_dict:
            video_dir = ''.join(key.split()) # 去掉字符串中间的空格
            self.title = os.path.join(base_dir, video_dir) 
            if base_dir not in os.listdir():
                os.makedirs(base_dir)
            video_dir = os.path.split(self.title)[-1]
            print(video_dir)
            if video_dir not in os.listdir(base_dir):
                os.makedirs(self.title)
            elif '0.ts' in os.listdir(self.title):
                print('已下载ts文件')
                self.ts_to_wav()
                return

            # 得到m3u8地址
            html = self.get_page(self.video_dict[key]['video_url'])
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

                        self.parse_ts(html)

                    except Exception as err:
                        print(err)
                        print('缓存文件请求错误，请检查错误')
                        if not os.listdir(self.title):
                        	shutil.rmtree(self.title)
            else:
            	print('无法获取视频网页！')
            	if not os.listdir(self.title):
                    shutil.rmtree(self.title)
                        	
        # 只下单个视频文件
        '''  
        key = '国务院食品安全办 多数居民存在食品安全认知误区'
        html = self.get_page(self.video_dict.get(key))
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

                    video_dir = ''.join(key.split()) # 去掉字符串中间的空格
                    self.title = os.path.join(base_dir, video_dir) 

                    self.parse_ts(html)
                except Exception as err:
                    print(err)
                    print('缓存文件请求错误，请检查错误')
        '''

    def parse_ts(self, html):
        pattern = re.compile('\d+.ts')
        self.ts_lists = re.findall(pattern, html)
        print(self.ts_lists)
        print('信息提取完成......\n准备下载...')
        self.pool()
        self.ts_to_wav()

    def pool(self):
        print('经计算需要下载%d个文件' % len(self.ts_lists))
        self.ts_url = self.m3u8_url[:-10]
        if base_dir not in os.listdir():
            os.makedirs(base_dir)
        video_dir = os.path.split(self.title)[-1]
        print(video_dir)
        if video_dir not in os.listdir(base_dir):
            os.makedirs(self.title)
        elif '0.ts' in os.listdir(self.title):
            print('已下载ts文件')
            return

        print('正在下载...所需时间较长，请耐心等待..')
        #开启多进程下载
        i = 0
        pool=Pool(16)
        pool.map(self.save_ts, [ts_list for ts_list in self.ts_lists])
        pool.close()
        pool.join()
        print('下载完成')

    def sort_key(self, s):
        if s:
            try:
                c = re.findall('\d+', s)[0]
            except:
                c = -1
            return int(c)

    def ts_to_wav(self):
        # 检测是否已存在wav文件
        video_dir = os.path.split(self.title)[-1]
        filename = os.path.join(dir_name, video_dir + '.wav')
        if dir_name not in os.listdir():
            os.makedirs(dir_name)
        elif os.path.isfile(filename):
            print('wav文件已存在')
            return

        # 开始格式转换
        print('ts文件正在进行转录wav......')
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
        # wav的格式必须是pcm_s16le
        str = 'ffmpeg -y -i "' + dirs + '" -vn -acodec pcm_s16le -f wav -ar 16000 ' + filename
        os.system(str)

        print(filename)
        if os.path.isfile(filename):
            print('转换完成')
            #shutil.rmtree(self.title)
        
    def save_ts(self, ts_list):
        try:
            ts_urls = self.ts_url + '/{}'.format(ts_list)
            print(ts_urls)
            urlretrieve(url=ts_urls, 
                filename=self.title + '/{}'.format(ts_list))
            time.sleep(1)
        except Exception as err:
            print(err)
            print('保存文件出现错误')


if __name__ == '__main__':
    # 工作目录设为yiner_src
    # pwd = os.getcwd()
    # if not pwd == working_path:
    #     os.chdir(working_path)
    # print(os.getcwd())
    
    # 开始爬虫
    cctv_spider()
