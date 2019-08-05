import os

from wechatsogou.const import WechatSogouConst
from wechatsogou.api import WechatSogouAPI
from wechatsogou.identify_image import identify_image_callback_by_hand
from rk import identify_image_callback_ruokuai_sogou, identify_image_callback_ruokuai_weixin

ws_api = WechatSogouAPI(captcha_break_time=3)
# 验证码输入错误的重试次数，默认为1
# 所有requests库的参数都能在这用
# 如 配置代理，代理列表中至少需包含1个 HTTPS 协议的代理, 并确保代理可用
# 如 设置超时
# ws_api = wechatsogou.WechatSogouAPI(captcha_break_time=3, proxies={
#     "http": "127.0.0.1:8888",
#     "https": "127.0.0.1:8888",
# }, timeout=3)
identify_image_callback_sogou = identify_image_callback_ruokuai_sogou if os.environ.get(
    'WechatSogouCI') else identify_image_callback_by_hand
identify_image_callback_ruokuai_weixin = identify_image_callback_ruokuai_weixin if os.environ.get(
    'WechatSogouCI') else identify_image_callback_by_hand
gzh_article = ws_api.get_gzh_article_by_history("中国食品网",
                                                identify_image_callback_sogou=identify_image_callback_sogou,
                                                identify_image_callback_weixin=identify_image_callback_ruokuai_weixin)

# gzh_article = ws_api.search_article("食品")
result = ws_api.search_article('食品', identify_image_callback=identify_image_callback_by_hand)
print(len(gzh_article['article']))
for article in gzh_article['article']:
    print(article['title'])
print(gzh_article['article'])
