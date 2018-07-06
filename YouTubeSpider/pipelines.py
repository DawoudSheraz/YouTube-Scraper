# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.contrib.exporter import CsvItemExporter


class YoutubespiderPipeline(object):

    def __init__(self):
        """
        Define the CSVItemExporter for the YouTubeDataModel.

        Item Exportation, file encoding and the sequence of fields defined.
        """
        self.csv_exporter = CsvItemExporter(open('data-master.csv', 'wb'))
        self.csv_exporter.encoding = 'utf-8'
        self.csv_exporter.fields_to_export = ['url', 'title'
                                              , 'views', 'likes', 'dislikes'
                                              , 'channel_name', 'publish_date'
                                              , 'channel_subscriber_count']

        self.csv_exporter.start_exporting()

    def spider_closed(self, spider):
        self.csv_exporter.finish_exporting()

    def process_item(self, item, spider):
        """
        Exports item through Item Exporter

        :param item: containing the data
        :param spider: spider that extracted and saved inside item
        :return: the item itself
        """
        self.csv_exporter.export_item(item)
        return item
