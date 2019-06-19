from selenium import webdriver
import time , requests
from lxml import etree
from pyquery import PyQuery as pq
import re


#此url通过Fiddler抓包获得，pass_ticket半个小时内有效 ，若失效则需要重新获取。
url='https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzA4ODgyMzY5Nw==&scene=124&uin=MTg3OTAxNTQ2NQ%3D%3D&key=f7bb43d4492422e05dfc5f60060621c66ffdbf67b93fb0f4d738f7ec89827bb99a8fb187a1f472bad521fe00a7cc1bdf85954198864d03b2cdc08aaa874c5d3409ef5f1bf5b8056df40016c60eec6606&devicetype=Windows+10&version=62060739&lang=zh_CN&a8scene=7&pass_ticket=c%2Bkq0P1x5aT3F5f%2BlhWVuR8zRknoktk9jrksUS3jBaAkVyNtrEu%2FPjgipbabPlLh&winzoom=1'
# Chromedriver
opt = webdriver.ChromeOptions()
# prefs = {'profile.default_content_setting_values': {'images': 2}}
# opt.add_experimental_option('prefs', prefs)#这两行是关闭图片加载
opt.add_argument('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat QBCore/3.43.884.400 QQBrowser/9.0.2524.400')#设置headers
# # opt.add_argument('--headless')#此行打开无界面
driver = webdriver.Chrome(chrome_options=opt,executable_path='E:\soft\chromedriver_win32\chromedriver.exe')

#river.add_cookie({'pgv_pvi': 'key-3200626688'}, {'RK': 'DZR8/DNdWQ'},{'ptcz': 'DZR8/d2481a1abe27c76c1f1ac777c6138f115b0e91286cd3c2e636093788fbd60344'},
                  #{'pgv_pvid':'513081676'},{'o_cookie':'997813969'},{"pac_uid","1_997813969"},
# {"tvfe_boss_uuid":"eaf59916385cdbc5"},{"wxuin":"1879015465"},{"devicetype":"Windows10"},{"version","62060739"},
# {"lang","zh_CN"},{"pass_ticket","5cTqye6YAqeNsJinNa1RI9QVlphivRwqeX+SkfjHaQSPa/ngPLG5ZtsrC1O0xetV"},{"wap_sid2","CKmA/v8GElxUdWV2YkhueE5jNUcySWNuVlo0d1JPZ3lub1RnVXZOMEt5andadW4zWU5lLWRQNjNlVmxXUVlPOHMxdHdFTUpCREU4SHZ0cThYTTJwQjFOcUgxY0YtLThEQUFBfjCwl7vmBTgNQJVO"})
# driver.delete_all_cookies()
#
# driver.add_cookie({"name":"pgv_pvi","value":"key-3200626688"})
# driver.add_cookie({"name":"RK","value":"DZR8/DNdWQ"})
# driver.add_cookie({"name":"ptcz","value":"DZR8/d2481a1abe27c76c1f1ac777c6138f115b0e91286cd3c2e636093788fbd60344"})
# driver.add_cookie({"name":"pgv_pvid","value":"513081676"})
# driver.add_cookie({"name":"o_cookie","value":"997813969"})
# driver.add_cookie({"name":"pac_uid","value":"1_997813969"})
# driver.add_cookie({"name":"tvfe_boss_uuid","value":"eaf59916385cdbc5"})
# driver.add_cookie({"name":"1879015465","value":"1879015465"})
# driver.add_cookie({"name":"devicetype","value":"Windows10"})
# driver.add_cookie({"name":"version","value":"62060739"})
# driver.add_cookie({"name":"lang","value":"zh_CN"})
# driver.add_cookie({"name":"pass_ticket","value":"5cTqye6YAqeNsJinNa1RI9QVlphivRwqeX+SkfjHaQSPa/ngPLG5ZtsrC1O0xetV"})
#driver.add_cookie({"name":"wap_sid2","value":"CKmA/v8GElxUdWV2YkhueE5jNUcySWNuVlo0d1JPZ3lub1RnVXZOMEt5andadW4zWU5lLWRQNjNlVmxXUVlPOHMxdHdFTUpCREU4SHZ0cThYTTJwQjFOcUgxY0YtLThEQUFBfjCwl7vmBTgNQJVO"})


driver.get(url)

top = 1
while 1:
    html = etree.HTML(driver.page_source)
    downss = html.xpath('//*[@id="js_nomore"]/div/span[1]/@style')
    bodyContent = html.xpath('//*[@id="js_history_list"]/div/div/div/div/h4/@hrefs')  # 获取文章的所有链接
    with open('./aother.txt', 'a+', encoding='utf-8') as fp:
        for i in bodyContent:
            print(str(i))
            fp.write(str(i) + "\n")
    if downss[0] == "display: none;":
        time.sleep(0.5)
        js = "var q=document.documentElement.scrollTop="+str(top*2000)
        driver.execute_script(js)#模拟下滑操作
        top += 1
        time.sleep(1)
    else:
        break
html = etree.HTML(driver.page_source)
bodyContent = html.xpath('//*[@id="js_history_list"]/div/div/div/div/h4/@hrefs')#获取文章的所有链接
print(bodyContent)
#保存本地
with open('./aother.txt','a+',encoding='utf-8') as fp:
    for i in bodyContent:
        print(str(i))
        fp.write(str(i) + "\n")
driver.close()
