# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import csv


class YoutubespiderPipeline(object):

    def __init__(self):
        self.csvwriter = csv.writer(open('data.csv', 'wb'))
        self.csvwriter.writerow(('URL,Title,Views,Likes,Dislikes,Channel Name,'
                                'Subscribers,Publish Date').split(','))

    def process_item(self, item, spider):
        """
        Saves Item data entry as csv

        :param item: containing the data
        :param spider: spider that extracted and saved inside item
        :return: the item itself
        """
        # Encode each entry to cater for non-English characters
        for key, value in item.iteritems():
            try:
                item[key] = value.encode('UTF-8')
            except AttributeError:      # Skip the empty values
                pass

        self.csvwriter.writerow([
                                 item['url'],
                                 item['title'],
                                 item['views'],
                                 item['likes'],
                                 item['dislikes'],
                                 item['channel_name'],
                                 item['channel_subscriber_count'],
                                 item['publish_date']
                                ])
        return item
