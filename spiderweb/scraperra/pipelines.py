# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pathlib import Path
import xlsxwriter


class ScraperraPipeline:

    def __init__(self):
        self.wb = None
        self.ws = None
        self.current_row_index = 0
        self.THIS_FOLDER = Path(__file__).parent.resolve()

    def process_item(self, item, spider):

        adapter = ItemAdapter(item)
        d = adapter.asdict()


        if self.current_row_index == 0: #write header
            for col, value in enumerate(d.keys()):
                self.ws.write(self.current_row_index, col, value)

        data = d.values()

        for col, value in enumerate(data):
            self.ws.write(self.current_row_index+1, col, value)

        self.current_row_index += 1

        return item

    def open_spider(self, spider):
        spider.logger.info('IN OPEN SPIDER')
        self.wb = xlsxwriter.Workbook(f'{self.THIS_FOLDER}/outputnew.xlsx')
        self.ws = self.wb.add_worksheet()

    def close_spider(self, spider):
        spider.logger.info('IN CLOSE SPIDER')
        self.ws.autofit()
        self.wb.close()