import urllib3
from selenium import webdriver
def test():
    # http=urllib3.PoolManager()
    # response=http.request('GET','https://new.qq.com/cmsn/20140917/20140917005892')
    # print (response.data)
    browser = webdriver.Chrome(executable_path='E:\soft\chromedriver_win32\chromedriver.exe')
    browser.get('https://new.qq.com/cmsn/20140917/20140917005892')
    print(browser.page_source)
if __name__=="__main__":
    test()
    "https://translate.googleapis.com/translate_a/t?anno=3&client=te_lib&format=html&v=1.0&key=AIzaSyBOti4mM-6x9WDnZIjIeyEU21OpBXqWBgw&logld=vTE_20181015_01&sl=en&tl=zh-CN&sp=nmt&tc=1&sr=1&tk=793212.693792&mode=1"

