#coding=utf-8
import scrapy
from scrapy.selector import Selector
from News.items import NewsItem
import re
from scrapy import Request
import json
from lxml import etree
import os
class WenshuNews(scrapy.Spider):
    name='wenshu'
    #keyword='瘦肉精'
    #page=1
    #start_url='https://www.sogou.com/sogou?site=news.qq.com&query='+keyword+'&page='+str(page)
   # start_urls=[
   #     start_url
   # ]
    hasNext = True
    def start_requests(self):
        start_url = 'http://www.pkulaw.cn/case/FullText/_getFulltext'
        headers={
       # 'Cookie':'ASP.NET_SessionId=olaap31rcup0a4bj2txrpk1o; CookieId=olaap31rcup0a4bj2txrpk1o; FWinCookie=1; Catalog_Search=undefined; Hm_lvt_58c470ff9657d300e66c7f33590e53a8=1545383261,1545383329; CheckIPAuto=0; CheckIPDate=2018-12-21 17:09:51; click0=2018/12/21 17:38:29; Hm_lpvt_58c470ff9657d300e66c7f33590e53a8=1545385192; ASP.NET_SessionId=olaap31rcup0a4bj2txrpk1o; CookieId=olaap31rcup0a4bj2txrpk1o; FWinCookie=1; Catalog_Search=undefined; Hm_lvt_58c470ff9657d300e66c7f33590e53a8=1545383261,1545383329; CheckIPAuto=0; CheckIPDate=2018-12-21 17:09:51; click0=2018/12/21 17:38:29; click1=2018/12/21 18:02:34; Hm_lpvt_58c470ff9657d300e66c7f33590e53a8=1545386596',
        'Cookie':'ASP.NET_SessionId=olaap31rcup0a4bj2txrpk1o; CookieId=olaap31rcup0a4bj2txrpk1o; FWinCookie=1; Catalog_Search=undefined; Hm_lvt_58c470ff9657d300e66c7f33590e53a8=1545383261,1545383329; CheckIPAuto=0; CheckIPDate=2018-12-21 17:09:51; click0=2018/12/21 17:38:29; click1=2018/12/21 18:02:34; Hm_lpvt_58c470ff9657d300e66c7f33590e53a8=1545386596; ASP.NET_SessionId=olaap31rcup0a4bj2txrpk1o; CookieId=olaap31rcup0a4bj2txrpk1o; FWinCookie=1; Catalog_Search=undefined; Hm_lvt_58c470ff9657d300e66c7f33590e53a8=1545383261,1545383329; CheckIPAuto=0; CheckIPDate=2018-12-21 17:09:51; click0=2018/12/21 17:38:29; Hm_lpvt_58c470ff9657d300e66c7f33590e53a8=1545385192; ASP.NET_SessionId=olaap31rcup0a4bj2txrpk1o; FWinCookie=1; Hm_lvt_58c470ff9657d300e66c7f33590e53a8=1545383261,1545383329; click0=2018/12/21 17:38:29; CookieId=olaap31rcup0a4bj2txrpk1o; CheckIPAuto=0; CheckIPDate=2018-12-21 21:24:01; Hm_lpvt_58c470ff9657d300e66c7f33590e53a8=1545398688',
        'Host':'www.pkulaw.cn',
        'Origin':'http://www.pkulaw.cn',
        'Referer':'http://www.pkulaw.cn/case/pfnl_a6bdb3332ec0adc4bbd511554c137821a92100d8880b487cbdfb.html?match=Exact',
       # 'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
        }
        root = 'F:\\研-毕业论文\\2018_01_01-2018_12_18+002+1902++_log\\2018_01_01-2018_12_18+002+1902++_log'  # 读取的批量txt所在的文件夹的路径
        file_names = os.listdir(root)  # 读取文件夹下所有的txt的文件名
        file_ob_list = []  # 定义一个列表，用来存放刚才读取的txt文件名
        for file_name in file_names:  # 循环地给这些文件名加上它前面的路径，以得到它的具体路径
            fileob = root + '\\' + file_name  # 文件夹路径加上\\ 再加上具体要读的的txt的文件名就定位到了这个txt
            file_ob_list.append(
                fileob)  # 将路径追加到列表中存储  ['D:\\project\\kdxf\\data5\\2018_01_01-2018_12_18+002+1902++_log\\2.txt',。。。。]

        print(file_ob_list)  # 打印这个列表的内容到显示屏，不想显示的话可以去掉这句

        for file_ob in file_ob_list:  # 按顺序循环读取所有文件
            f = open(file_ob, 'r', encoding='UTF-8')
            for line in f.readlines():
                title=line.split()[0].split(u'、')[1]
                line1 = line.split()[1]  # 取这一行空格前者
                yield scrapy.FormRequest(
                        url=start_url,
                        formdata={"library": "pfnl", "gid": line1,
                                  "loginSucc": "0"},
                        callback=self.parse,
                        headers=headers,
                        meta={"title":title}
                    )
    def write2file(content, filename):  # 将爬取的文书写入文件保存
        try:
            f = open(filename, 'w')
        except Exception as e:
            filename = filename.split(u'、')[0] + '_error_filename.txt'
            f = open(filename, 'w')
        f.write(content.encode('utf-8'))
        f.close()
    def parse(self, response):
        # html_script=r'\<br\>([\w\/]+)$'
        # m_script = re.findall(html_script, response.body.decode('utf-8'), re.S | re.M)
        #sel=Selector(response)
        # header=sel.xpath('//p/font/text()').extract()
        # print (header)
        # body=sel.xpath('//div/text()').extract()
        # print (body)
        # text=sel.xpath('//br').extract()
        title=response.meta["title"]
        #print (title)
        page = etree.HTML(response.text)
        content = page.xpath('body')[0].xpath('string(.)')
        # text=response.body
        # print(response.text)
        # page = etree.HTML(response.text)
        # content = page.xpath('body')[0].xpath('string(.)').strip()
        # filepath='a6bdb3332ec0adc468dc78977a2ab00d1f8aaad646df15f7bdfb.txt'
        # try:
        #     f = open(filepath, 'w', encoding="utf-8")
        # except Exception as e:
        #     filename = filepath.split(u'、')[0] + '_error_filename.txt'
        #     f = open(filename, 'w')
        # f.write(content)
        # f.close()
        item=NewsItem()
        item['title'] = title
        item['content']=content
        yield item

