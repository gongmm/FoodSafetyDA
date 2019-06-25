#-*-coding:utf-8-*-
from selenium import webdriver
from lxml import etree
import requests
import random
import csv
#import BeautifulSoup

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
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'Cache-Control': 'max-age=0',
    'Proxy-Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': random.choice(UA_LIST),

}

allow_domain = 'http://bbs.foodmate.net/'
def luntan():

    keyword='非洲猪瘟'
    browser=webdriver.Chrome(executable_path='E:\soft\chromedriver_win32\chromedriver.exe')
    browser.get('http://bbs.foodmate.net/search.php?')
    input_key=browser.find_element_by_id('scform_srchtxt')
    input_key.clear()
    input_key.send_keys(keyword)
    button=browser.find_element_by_id('scform_submit')
    button.click()
    #h2=browser.window_handles
    #browser.switch_to.window(h2[1])
    sel=etree.HTML(browser.page_source)

    div_content=sel.xpath('//div[@id="threadlist"]/ul/li')
    for ul_content in div_content:
        title=ul_content.xpath(".//a/text()")
        titles=''
        for i in title:
            titles=titles+i
        print(titles)
        url=ul_content.xpath(".//a/@href")[0]
        print(url)
        time=ul_content.xpath('./p[3]/span[1]/text()')[0]
            #print(time)
        parse(url,titles,time)
    nextpage = sel.xpath("//div[@class='pg']")
    if nextpage:
        nextpage=sel.xpath("//div[@class='pg']/a/@href")[0]
        next_page(nextpage)
def parse(url,title,time):
    print ("parse"+url)

    contentpagesource = requests.get(allow_domain + url, headers=headers)
    contentsel = etree.HTML(contentpagesource.text)
    contents = contentsel.xpath('//div[@class="t_fsz"]//td[@class="t_f"]')
    reviewlist=[]
    for td_content in contents:
        review = td_content.xpath('./text()')[0]

        #review = td_content.xpath('./td[@class="t_f"]')
        print(review)
        reviewlist.append(review)
        '''存数据'''
    item={}
    item['time']=time
    item['title']=title
    item['reviews']=reviewlist
    save('luntan.csv',item)
    nextpage =contentsel.xpath('//div[@class="pgbtn"]')
    if nextpage:
        nextpage=contentsel.xpath('//div[@class="pgbtn"]/a/@href')[0]
        parse(nextpage,title,time)

def next_page(url):
    pagesource = requests.get(allow_domain + url, headers=headers)
    sel = etree.HTML(pagesource.text)
    div_content = sel.xpath('//div[@id="threadlist"]/ul/li')
    for ul_content in div_content:
        title = ul_content.xpath(".//a/text()")
        titles = ''
        for i in title:
            titles = titles + i
        print(titles)
        url = ul_content.xpath(".//a/@href")[0]
        print(url)
        time = ul_content.xpath('./p[3]/span[1]/text()')[0]
        # print(time)
        parse(url,titles,time)
    nextpage = sel.xpath("//div[@class='pg']")
    if nextpage:
        nextpage = sel.xpath("//div[@class='pg']/a/@href")[0]
        next_page(nextpage)
def save(filename,item):
    with open(filename, 'a+', encoding='utf-8', newline='') as f:
        # f = open(filename,'a+',encoding='utf-8',newline = '')
        writer = csv.writer(f, dialect="excel")
        writer.writerow([item['time'], item['title'], item['reviews']])

if __name__=='__main__':
    luntan()