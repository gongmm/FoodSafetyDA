#coding=utf-8
import scrapy
from selenium import webdriver
from scrapy.selector import Selector
from lxml import etree
import time
from News.items import NewsItem
class PeopleNews(scrapy.Spider):
    name="peopleNews"
    allowed_domain=['people.com.cn']
    page=1

    def start_requests(self):
        browser = webdriver.Chrome(executable_path='E:\soft\chromedriver_win32\chromedriver.exe')
        browser.get("http://www.people.com.cn/")
        input_key = browser.find_element_by_id('keyword')
        js = "var q=document.getElementById(\"p_search\");q.style.display = \"block\";"
        # 执行js
        browser.execute_script(js)
        input_key.clear()
        input_key.send_keys("地沟油")
        button = browser.find_element_by_xpath("//div[@id='p_search']/form/p[2]/input")
        print(button)
        button.click()
        h2 = browser.window_handles  # 获取句柄
        browser.switch_to.window(h2[1])
        # browser.implicitly_wait(5000)
        sel = etree.HTML(browser.page_source)
        i = 0
        try:
            while True:
                div_content = sel.xpath("//div[@class='w980']/div[@class='fr w800']/ul")
                for ul_content in div_content:
                    item=NewsItem()
                    title = ul_content.xpath("./li[1]/b/a/text()")[0]
                    print(type(title))
                    item['title']=title
                    url = ul_content.xpath("./li[1]/b/a/@href")[0]
                    item['url'] = url
                    #digest = ul_content.xpath("./li[2]/text()")[0]
                    digest_str = ""
                    #if len(digest) > 0:
                     #   for j in range(len(digest)):
                      #      digest_str = digest_str + ul_content.xpath("./li[2]/text()")[j]
                    #item['digest'] = digest
                   # pubdate = ul_content.xpath("./li[3]/text()")[0]
                    #item['pubdate'] = pubdate
                    return item
                print('-----------------------------')
                #scrapy.Request(url,callback=self.detail_parse,cookies=[])
                if i == 0:
                    next_page = browser.find_element_by_xpath("//div[@class='show_nav_bar']/a[10]")
                    i = i + 1
                else:
                    next_page = browser.find_element_by_xpath("//div[@class='show_nav_bar']/a[11]")
                next_page.click()
                windows = browser.window_handles  # 获取句柄
                browser.switch_to.window(windows[-1])  # 获取打开最新的窗口
                sel = etree.HTML(browser.page_source)
                time.sleep(5)
                # print(browser.page_source)
        except Exception as e:
            print(e.message)

            # browser.implicitly_wait(5000)
            # 获取所有窗口的句柄
            # 获取当前窗口的句柄
            # currentWin = browser.current_window_handle
            # handles = browser.window_handles
            # for i in handles:
            # if currentWin == i:
            #  continue
            # else:
            # 将driver与新的页面绑定起来
            # browser = browser.switch_to_window(i)
        browser.close()
