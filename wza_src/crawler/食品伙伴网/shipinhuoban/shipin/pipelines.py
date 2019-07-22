# -*- coding: utf-8 -*-

from openpyxl import Workbook

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import JsonItemExporter


class ShipinPipeline(object):
    wb = Workbook()
    ws = wb.active
    ws.append(['name', 'grant', 'amount', 'location', 'range'])

    def process_item(self, item, spider):  # 工序具体内容
        # 1. 写入的文件对象
        file = open("huoban.json", 'wb')
        # 2. 创建导出器
        exporter = JsonItemExporter(file)
        # 3. 开启导出器
        exporter.start_exporting()
        # 4. 导出数据
        exporter.export_item(item)
        # 5. 关闭导出器
        exporter.finish_exporting()
        # 6. 关闭文件
        file.close()
        # 导出表格操作
        line = [item['time'], item['link'], item['title'], item['content'], item['category']]  # 把数据每一行整理出来
        self.ws.append(line)  # 将数据一行的形式添加到xlsx中
        self.wb.save('data.xlsx')  # 保存xlsx文件
        return item
    # def open_spider(self, spider):
    #     self.conn = MongoClient(host='127.0.0.1', port=27017)
    #     self.client = self.conn.news.shipin
    #
    # def process_item(self, item, spider):
    #     if isinstance(item, ShipinItem):
    #         self.client.insert(dict(item))
    #         return item
