import requests


def get_ip():
    proxy_list = []
    with open('proxy6.txt', 'r') as f:
        for line in f.readlines():
            proxy_list.append(line.strip('\n'))
    return proxy_list


def judge_ip(ip):
    #  判断ip 是否可用
    # http_url = 'http://news.foodmate.net'
    # http_url = 'https://blog.csdn.net/sixkery/article/details/82726177'
    # http_url = 'https://www.baidu.com'
    http_url = 'http://www.eshian.com/sat/foodinformation/hync/articlelist/17/453/1'
    proxy_url = 'http://{0}'.format(ip)
    print("Testing: " + proxy_url)
    try:
        proxy_dict = {
            'http': proxy_url
        }
        r = requests.get(http_url, proxies=proxy_dict, timeout=5)
        print('effective ip')
        if 200 <= r.status_code < 300:
            print('effective ip')
            with open('valid.txt', 'a') as f:
                f.write(ip + '\n')
            return True
        else:
            print('invalid ip and port 无效')
            return False
    except Exception as e:
        print(str(e))
        return False


if __name__ == '__main__':
    list = get_ip()
    for ip in list:
        judge_ip(ip)
