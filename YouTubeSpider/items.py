# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field


class YouTubeDataModel(Item):

    """
    The class defines the item model to store the extracted data from YouTube
    """

    title = Field()
    likes = Field()
    dislikes = Field()
    views = Field()
    channel_name = Field()
    number_of_comments = Field()
    channel_subscriber_count = Field()
    publish_date = Field()
    url = Field()
