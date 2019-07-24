import csv
from urllib import request
from urllib import error
from bs4 import BeautifulSoup
import time
import socket
import sys
#将分类完毕的url写入文件
def write_csv(type,url_list):
    print('开始写文件')
    outfile = '/Users/Amanda/Desktop/大四/毕设/爬虫/url分类爬虫/urls/newspeople_' + type + '.csv'
    out = open(outfile, 'a')
    csv_write = csv.writer(out, dialect='excel')
    for url in url_list:
        # print(url)
        url_l = []
        url_l.append(url)  # 将url转为list格式
        csv_write.writerow(url_l)
    print('写文件完毕')

# 读取csv文件，将url保存为list
def read_csv():
    print('开始读取文件')
    filename = '/Users/Amanda/Desktop/大四/毕设/爬虫/url分类爬虫/newspeople.csv'  # 需要读取对的文件路径
    with open(filename, encoding="unicode_escape") as f:
        next(f)  # 跳过第一行
        f_csv = csv.reader(f)
        urls = []
        for row in f_csv:
            urls.append(row[2])  # 提取每行的第三列（url）
    print('读取完毕')
    return urls

#url分类主程序
def url_sort(urls):
    print('开始分类')
    url_list = []
    for url in urls:    #对每一个url进行判断
        print(url)
        count = 0   #标记retry次数
        max_retry_count = 5 #设置最大retry次数
        while(count < max_retry_count): #当链接请求超时，则在最大retry次数内重新请求
            try:
                html = request.urlopen(url,timeout=1)
                bf = BeautifulSoup(html, 'html.parser', from_encoding='gb18030')  # beautifulsoup解析网页
                div_bf = bf.find('div', attrs={'class': 'p2_left d2text_left'})  # 判断是否有该div
                if not div_bf:
                    pass
                else:
                    url_list.append(url)
                count = max_retry_count #如果成功请求，则退出while循环
            except socket.timeout as e:
                count = count+1 #每次超时，count+1
                print(str(e))
            except Exception as e:
                count = max_retry_count
                print(str(e))
    print('分类完毕')
    return url_list

#入口函数
def sort_run():
    start =time.clock()
    url_list=url_sort(read_csv())
    write_csv('10',url_list)
    end = time.clock()
    print('Running time: %s Seconds'%(end-start))

sort_run()





