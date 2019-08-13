# coding=utf-8

"""

功能: 爬取新浪微博的搜索结果,支持高级搜索中对搜索时间的限定
网址：http://s.weibo.com/
实现：采取selenium测试工具，模拟微博登录，结合PhantomJS/Firefox，分析DOM节点后，采用Xpath对节点信息进行获取，实现重要信息的抓取

"""
import csv
import io
import os
import sys
import time
import datetime
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

option = webdriver.ChromeOptions()
option.add_argument(r"user-data-dir=C:\Users\gnaiz\AppData\Local\Google\Chrome\User Data 3")
# option.add_argument(r"user-data-dir=C:\Users\Administrator\AppData\Local\Google\Chrome\User Data 4")
driver = webdriver.Chrome(chrome_options=option)
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')  # 改变标准输出的默认编码

# driver = webdriver.Chrome()


# ********************************************************************************
#                            第一步: 登陆login.sina.com
#                     这是一种很好的登陆方式，有可能有输入验证码
#                          登陆之后即可以登陆方式打开网页
# ********************************************************************************

def LoginWeibo(username, password):
    try:
        # 输入用户名/密码登录
        print('准备登陆Weibo.cn网站...')
        driver.get('http://weibo.com/login.php')
        driver.implicitly_wait(5)
        elem_user = driver.find_element_by_xpath('//*[@id="loginname"]')
        elem_user.clear()
        elem_user.send_keys(username)  # 用户名
        elem_pwd = driver.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[2]/div/input')
        elem_pwd.clear()
        elem_pwd.send_keys(password)  # 密码
        time.sleep(5)
        elem_sub = driver.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[6]/a')

        try:
            # 输入验证码
            time.sleep(20)
            elem_sub.click()
        except:
            # 不用输入验证码
            pass

        # 获取Coockie 推荐资料：http://www.cnblogs.com/fnng/p/3269450.html
        print('Crawl in ' + driver.current_url)
        print('输出Cookie键值对信息:')
        for cookie in driver.get_cookies():
            print(cookie)
            for key in cookie:
                print(key + cookie[key])
        print('登陆成功...')
    except Exception as e:
        print("Error: " + str(e))
    finally:
        print('End LoginWeibo!')


# ********************************************************************************
#                  第二步: 访问http://s.weibo.com/页面搜索结果
#               输入关键词、时间范围，得到所有微博信息、博主信息等
#                     考虑没有搜索结果、翻页效果的情况
# ********************************************************************************

def GetSearchContent(key, topic_id):
    driver.get("http://s.weibo.com/")
    print('搜索热点主题：'+ key)

    # 输入关键词并点击搜索
    # item_inp = driver.find_element_by_xpath("//input[@class='searchInp_form']")
    item_inp = driver.find_element_by_xpath("//div[@class='search-input']/input")
    item_inp.send_keys(key)
    item_inp.send_keys(Keys.RETURN)  # 采用点击回车直接搜索

    # 获取搜索词的URL，用于后期按时间查询的URL拼接
    current_url = driver.current_url
    current_url = current_url.split('&')[
        0]  # http://s.weibo.com/weibo/%25E7%258E%2589%25E6%25A0%2591%25E5%259C%25B0%25E9%259C%2587

    global start_stamp
    global page

    # 需要抓取的开始和结束日期
    start_date = datetime.datetime(2018, 8, 1, 0)
    end_date = datetime.datetime(2018, 9, 1, 0)
    delta_date = datetime.timedelta(hours=6)

    # 每次抓取一天的数据
    start_stamp = start_date
    end_stamp = start_date + delta_date
    file_name = 'data/weibo_topic'+ str(topic_id) + '.csv'
    if not os.path.exists(file_name):
        init_csv(writefile=file_name)
    while end_stamp <= end_date:
        page = 1

        # 每一天使用一个sheet存储数据
        # sheet = outfile.add_sheet(str(start_stamp.strftime("%Y-%m-%d-%H")))
        # initXLS()

        # 通过构建URL实现每一天的查询
        url = current_url + '&typeall=1&suball=1&timescope=custom:' + str(
            start_stamp.strftime("%Y-%m-%d-%H")) + ':' + str(end_stamp.strftime("%Y-%m-%d-%H")) + '&Refer=g'
        driver.get(url)
        handlePage(file_name)  # 处理当前页面内容

        start_stamp = end_stamp
        end_stamp = end_stamp + delta_date


# ********************************************************************************
#                  辅助函数，考虑页面加载完成后得到页面所需要的内容
# ********************************************************************************

# 页面加载完成后，对页面内容进行处理
def handlePage(file_name):
    while True:
        # 之前认为可能需要sleep等待页面加载，后来发现程序执行会等待页面加载完毕
        # sleep的原因是对付微博的反爬虫机制，抓取太快可能会判定为机器人，需要输入验证码
        time.sleep(1)
        # 先行判定是否有内容
        if checkContent():
            print("getContent")
            getContent(file_name)
            # 先行判定是否有下一页按钮
            if checkNext():
                # 拿到下一页按钮
                next_page_btn = driver.find_element_by_xpath("//a[@class='next']")
                next_page_btn.click()
                # time.sleep(5)
            else:
                print("no Next")
                break
        else:
            print("no Content")
            break


# 判断页面加载完成后是否有内容
def checkContent():
    # 有内容的前提是有“导航条”？错！只有一页内容的也没有导航条
    # 但没有内容的前提是有“pl_noresult”
    try:
        driver.find_element_by_xpath("//div[@class='card-no-result']")
        flag_1 = False
    except:
        flag_1 = True

    try:
        driver.find_element_by_xpath("//div[@class='m-error']")
        flag_2 = False
    except:
        flag_2 = True
    return flag_1 and flag_2


# 判断是否有下一页按钮
def checkNext():
    try:
        driver.find_element_by_xpath("//a[@class='next']")
        flag = True
    except:
        flag = False
    return flag


# 在添加每一个sheet之后，初始化字段
def init_csv(writefile='data/weibo_search_result_africa_fever.csv'):
    name = ['nick_name', 'homepage_url', 'certification', 'content', 'pub_date', 'repost', 'comment', 'like']
    with open(writefile, 'w', encoding='utf-8', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(name)


# 将dic中的内容写入excel
def write_to_csv(dic, writefile='data/weibo_search_result_africa_fever.csv'):
    print("=====正在写入=====")
    with open(writefile, 'a', encoding='utf-8', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        for item in dic.values():
            csv_writer.writerow(item)
    print("=====写入完成=====")

# 在页面有内容的前提下，获取内容
def getContent(file_name):
    # 寻找到每一条微博的class
    nodes = driver.find_elements_by_xpath("//div[@class='card']")

    # 在运行过程中微博数==0的情况，可能是微博反爬机制，需要输入验证码
    if len(nodes) == 0:
        # driver.refresh()
        input("请在微博页面输入验证码！")
        url = driver.current_url
        driver.get(url)
        getContent(file_name)
        return

    dic = {}

    global page
    print(str(start_stamp.strftime("%Y-%m-%d-%H")))
    print('页数: ' + str(page))
    page = page + 1
    print('微博数量' + str(len(nodes)))

    for i in range(len(nodes)):
        dic[i] = []

        try:
            info = nodes[i].find_element_by_xpath(".//div[@class='info']")
            BZNC = info.find_element_by_xpath("./div[2]/a[1]").text
        except:
            BZNC = ''
        print('博主昵称:' + BZNC)
        dic[i].append(BZNC)

        try:
            BZZY = nodes[i].find_element_by_xpath(
                ".//div[@class='info']/div[2]/a[1]").get_attribute("href")
        except:
            BZZY = ''
        print('博主主页:' + BZZY)
        dic[i].append(BZZY)

        try:
            WBRZ = nodes[i].find_element_by_xpath(
                ".//div[@class='info']/div[2]/a[2]").get_attribute('title')  # 若没有认证则不存在节点
        except:
            WBRZ = ''
        print('微博认证:' + WBRZ)
        dic[i].append(WBRZ)

        try:
            WBNR = nodes[i].find_element_by_xpath(".//div[@class='content']/p[@class='txt']").text
        except:
            WBNR = ''
        # print('微博内容:' + WBNR)
        dic[i].append(WBNR)

        try:
            FBSJ = nodes[i].find_element_by_xpath(".//div[@class='content']/p[@class='from']/a[1]").text
        except:
            FBSJ = ''
        print('发布时间:' + FBSJ)
        dic[i].append(FBSJ)

        try:
            ZF_TEXT = nodes[i].find_element_by_xpath(".//div[@class='card-act']//li[2]").text
            if len(re.findall('\d', ZF_TEXT)) == 0:
                ZF = 0
            else:
                ZF = ''
                for num in re.findall('\d', ZF_TEXT):
                    ZF += num
                ZF = int(ZF)

        except:
            ZF = 0
        print('转发:' + str(ZF))
        dic[i].append(str(ZF))

        try:
            PL_TEXT = nodes[i].find_element_by_xpath(".//div[@class='card-act']//li[3]").text
            if len(re.findall('\d', PL_TEXT)) == 0:
                PL = 0
            else:
                PL = ''
                for num in re.findall('\d', PL_TEXT):
                    PL += num
                PL = int(PL)
        except:
            PL = 0
        print('评论:' + str(PL))
        dic[i].append(str(PL))

        try:
            ZAN_TEXT = nodes[i].find_element_by_xpath(".//div[@class='card-act']//li[4]").text  # 可为空
            if len(re.findall('\d', ZAN_TEXT)) == 0:
                ZAN = 0
            else:
                ZAN = ''
                for num in re.findall('\d', ZAN_TEXT):
                    ZAN += num
                ZAN = int(ZAN)
        except:
            ZAN = 0
        print('赞:' + str(ZAN))
        dic[i].append(str(ZAN))

    # 写入Excel
    write_to_csv(dic, file_name)


def get_keywords(start, end):
    id_list = []
    word_list = []
    with open('keywords.txt', 'r', encoding='GBK') as f:
        for info in f.readlines():
            topic_id = info.split(',')[0]
            topic_word = info.split(',')[-1].strip()
            id_list.append(topic_id)
            word_list.append(topic_word)
    return id_list[start:end+1], word_list[start:end+1]

# *******************************************************************************
#                                程序入口
# *******************************************************************************
if __name__ == '__main__':
    # 定义变量
    username = 'yulianwei1011@126.com'  # 输入你的用户名
    password = 'fsda123'  # 输入你的密码

    # 操作函数
    LoginWeibo(username, password)  # 登陆微博

    # id_list, word_list = get_keywords(0, 8)
    # id_list, word_list = get_keywords(9, 17)
    # id_list, word_list = get_keywords(18, 26)
    id_list, word_list = get_keywords(32, 35)

    for index in range(len(word_list)):
        # 搜索热点微博 爬取评论
        # key = '非洲猪瘟'
        GetSearchContent(word_list[index], id_list[index])
