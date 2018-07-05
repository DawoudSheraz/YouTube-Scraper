# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join
from w3lib.html import remove_tags


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


def white_space_stripper(x):
    """
    Removes white spaces.
    Called as input to MapCompose
    :param x: string
    :return: string without whitespaces
    """
    return x.strip()


def view_number_extractor(view_string):
    out_val = view_string
    try:
        out_val = view_string.split()[0]
    except ValueError:
        pass
    return out_val


def date_value_extractor(date_string):
    out_val = date_string
    try:
        out_val = date_string.split()[2:]
    except ValueError:
        pass
    return out_val


class YoutubeItemLoader(ItemLoader):

    default_output_processor = Join()
    default_input_processor = MapCompose(remove_tags)

    title_in = MapCompose(remove_tags, white_space_stripper)

    views_in = MapCompose(view_number_extractor)

    likes_in = MapCompose(remove_tags)

    dislikes_in = MapCompose(remove_tags)

    channel_name_in = MapCompose(remove_tags, white_space_stripper)

    publish_date_in = MapCompose(remove_tags, date_value_extractor)
