import requests
from urllib.parse import urlencode
from urllib import parse
start_url = 'https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D1%26q%3D%E7%8C%AA%E8%82%89+%E5%B1%A0%E5%AE%B0+%E7%89%9B%E8%82%89&page_type=searchall&page=1'
url_prefix = 'https://m.weibo.cn/api/container/getIndex?'
params = {
    'containerid': '100103type=1&q=猪肉 屠宰 牛肉',
    'page_type': 'searchall',
    'page': 1
}
#print(parse.quote('猪肉 屠宰 牛肉'))
#start_url = url_prefix +'containerid=100103type%3D1%26q'+parse.quote('猪肉 屠宰 牛肉')+'&page_type=searchall&page=1'
start_url=url_prefix+urlencode(params)
print(start_url)
#response=requests.get("https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D1%26q%3D%E7%8C%AA%E8%82%89+%E5%B1%A0%E5%AE%B0+%E7%89%9B%E8%82%89&page_type=searchall")
response=requests.get(start_url)
import json
jsondata=json.loads(response.text)
txt=jsondata['data']['cards']
print (txt)