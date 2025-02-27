from Crawler import Crawl


####################################################################################
# 将分别属于两个主题的关键词列表中的词汇两两组合进行搜索，可以爬取到同时包含两个主题中关键词的文章
####################################################################################
def crawl():
    # keywords = [
    #     [
    #         '疟疾', '腹泻', '感染', '疾病', '肺炎', '流行病',
    #         '公共卫生', '流行病学', '卫生保健', '卫生', '死亡率', '发病率', '营养', '疾病',
    #         '非传染性疾病', '传染性疾病', '传染病', '空气污染',
    #         '精神障碍', '发育迟缓',
    #         '传染', '疾患', '症', '病', '瘟疫', '流感', '流行感冒', '治疗', '保健', '健康', '死亡'],
    #     ['气候变化', '全球变暖', '温室', '极端天气', '全球环境变化',
    #      '低碳', '可再生能源', '碳排放', '二氧化碳排放', '气候污染',
    #      '气候', '全球升温', '再生能源', 'CO2排放']]

    keywords = [['食品安全']]
    crawler = Crawl(keywords)
    crawler.crawl_complex_search()


if __name__ == '__main__':
    crawl()
