# -*- coding: utf-8 -*-
import scrapy
import re


class WeChatSogouSpider(scrapy.Spider):
    name = "WeChat"
    allowed_domains = ["weixin.sogou.com", 'mp.weixin.qq.com']
    start_urls = ['http://weixin.sogou.com/']

    def parse(self, response):

        wx_source = ["1-食品"]
        for v_wx_source in wx_source:
            print('wx_source ===', v_wx_source)
            try:
                type = v_wx_source.split('-')[0]
                channel = v_wx_source.split('-')[1]
                print("正在抓取:", type, channel)
                v_main_url = 'http://weixin.sogou.com/weixin?type=1&s_from=input&query={}'.format(channel)
                print('v_main_url', v_main_url)
                yield scrapy.Request(url=str(v_main_url), callback=self.parse_main_link, meta={'type': type})
            except:
                print('wx_source error ===', v_wx_source)
                continue

    def parse_main_link(self, response):
        print('parse_main_link ====  ', response.body)
        target_url = response.xpath("//*['txt-box']/p[@class='tit']/a/@href").extract_first()
        print('===== start =====')
        print('target_url', target_url)
        print('==== end =====')
        if target_url:
            yield scrapy.Request(url=target_url, callback=self.parse_list_gzhao)

    def parse_list_gzhao(self, response):
        print('resonse:  ', response)
        req_text = response.text

        reg_content_url = r'"content_url":"(.*?)",'
        m_infos = re.findall(reg_content_url, req_text, re.S)
        print(len(m_infos))
        for v_info in m_infos:
            v_info = 'https://mp.weixin.qq.com' + re.sub('&amp;', '&', v_info)
            print(v_info)
            yield scrapy.Request(url=v_info, callback=self.parse_detail)

    def parse_detail(self, response):
        print('parse_detail ===== ', response.text)
