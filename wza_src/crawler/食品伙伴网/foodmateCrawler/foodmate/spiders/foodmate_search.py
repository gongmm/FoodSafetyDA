import scrapy
from scrapy import Request
from scrapy import Selector
from foodmate.items import FoodMateItem


class FoodMateNews(scrapy.Spider):
    name = 'foodmate_search'
    headers = {
        'Cookie': '__gads=ID=b18bbac9635253d1:T=1541734640:S=ALNI_MZ2wateVMtYJQWkVvaft4QR8WBmlA; bc08_f0d8_saltkey=ndQrdqHd; bc08_f0d8_lastvisit=1545374191; bc08_f0d8_lastact=1546591460%09api.php%09js; Hm_lvt_2aeaa32e7cee3cfa6e2848083235da9f=1545377836,1545827373,1546502726,1546591464; __51cke__=; u_last_search=1546593161; yunsuo_session_verify=cd11db7b21b1480cb734c3076363d1cc; Hm_lpvt_2aeaa32e7cee3cfa6e2848083235da9f=1546593163; __tins__1636283=%7B%22sid%22%3A%201546591465709%2C%20%22vd%22%3A%2018%2C%20%22expires%22%3A%201546594962572%7D; __51laig__=18'
    }
    keyword = '地沟油'
    page = 1
    start_url = 'http://news.foodmate.net/search.php?kw=' + keyword + '&page=' + str(page)
    url_prefix = 'http://news.foodmate.net/search.php?kw=' + keyword + '&page='

    def start_requests(self):

        yield Request(url=self.start_url, headers=self.headers, callback=self.parse)

    def parse(self, response):
        sel = Selector(response)
        li_list = sel.xpath("//div[@class='catlist']/ul/li[@class='catlist_li']")
        for li_content in li_list:
            link = li_content.xpath("./a/@href").extract()[0]
            title = li_content.xpath("./a/@title").extract()[0]
            time = li_content.xpath("./span/text()").extract()[0]
            if "2018-01-01 00:00" < time < "2019-01-01 00:00":
                yield Request(url=link, meta={'title': title, 'link': link, 'time': time}, callback=self.parse_content)
            else:
                pass
        self.page = self.page + 1

        # pagenumstr = sel.xpath('//cite/text()').extract()
        # page_num = "共1285条/26页".split('/')[1][:-3]
        # if self.page <= page_num:

        print(self.url_prefix + str(self.page))
        yield Request(url=self.url_prefix + str(self.page) + ".html", headers=self.headers, callback=self.parse)

    @staticmethod
    def parse_content(response):
        sel = Selector(response)
        content = sel.xpath("//div[@id='article']//text()").extract()
        content_str = ""
        for c in content:
            content_str = content_str + c.strip()
        tags = sel.xpath("//font[@class='gjc_g'][3]/following-sibling::a//font[@class='gjc_c']/text()").extract()
        tag_str = ""
        for tag in tags:
            tag_str = tag_str + " " + tag
        category = sel.xpath("//font[@class='gjc_g'][2]/following-sibling::a//font[@class='gjc_c']/text()").extract()
        category_str = ""
        for word in category:
            if word not in tags:
                category_str = category_str + " " + word
        areas = sel.xpath("//font[@class='gjc_g'][1]/following-sibling::a//font[@class='gjc_c']/text()").extract()
        area_str = ""
        for word in areas:
            if word not in category:
                area_str = area_str + " " + word
        title = response.meta['title']
        time = response.meta['time']
        link = response.meta['link']

        item = FoodMateItem()
        item['title'] = title
        item['time'] = time
        item['link'] = link
        item['category'] = category_str
        item['tags'] = tag_str
        item['area'] = area_str
        item['content'] = content_str
        yield item
        print(tag_str)
        print(category_str)
        print(area_str)
