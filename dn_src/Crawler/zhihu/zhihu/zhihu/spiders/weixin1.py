import requests

url = "https://mp.weixin.qq.com/mp/profile_ext"

querystring = {"action":"home","__biz":"MzA4ODgyMzY5Nw==","scene":"124"}

headers = {
    'cookie': "pgv_pvi=3200626688; RK=DZR8/DNdWQ; ptcz=d2481a1abe27c76c1f1ac777c6138f115b0e91286cd3c2e636093788fbd60344; pgv_pvid=513081676; o_cookie=997813969; pac_uid=1_997813969; tvfe_boss_uuid=eaf59916385cdbc5; wxuin=1879015465; devicetype=Windows10; version=62060739; lang=zh_CN; pass_ticket=5cTqye6YAqeNsJinNa1RI9QVlphivRwqeX+SkfjHaQSPa/ngPLG5ZtsrC1O0xetV; wap_sid2=CKmA/v8GElxUdWV2YkhueE5jNUcySWNuVlo0d1JPZ3lub1RnVXZOMEt5andadW4zWU5lLWRQNjNlVmxXUVlPOHMxdHdFTUpCREU4SHZ0cThYTTJwQjFOcUgxY0YtLThEQUFBfjCwl7vmBTgNQJVO; rewardsn=; wxtokenkey=777",
    'cache-control': "no-cache",
    'postman-token': "1d2abb74-5f8b-f0aa-727d-36a041156a3a"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)