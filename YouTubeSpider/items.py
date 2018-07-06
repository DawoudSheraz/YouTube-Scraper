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


def remove_commas(x):

    out_val = x
    try:
        out_val = x.replace(',', '').replace(';', '')
    except:
        pass
    return out_val


def view_number_extractor(view_string):
    """
    Gets view number from Extracted view string.
    """
    out_val = view_string
    try:
        out_val = view_string.split()[0]
    except IndexError:
        pass
    return out_val


def date_value_extractor(date_string):
    """
    Gets date  from Extracted date string.
    """
    out_val = date_string
    try:
        out_val = date_string.split()[2:]
    except IndexError:
        pass
    return out_val


class YoutubeItemLoader(ItemLoader):

    """
    Item Loader class for YouTubeDataModel Item.
    """

    default_output_processor = Join()
    default_input_processor = MapCompose(remove_tags)

    title_in = MapCompose(remove_tags, white_space_stripper)

    views_in = MapCompose(view_number_extractor, remove_commas)

    likes_in = MapCompose(remove_tags, remove_commas)

    dislikes_in = MapCompose(remove_tags, remove_commas)

    channel_name_in = MapCompose(remove_tags, white_space_stripper
                                 , remove_commas)

    publish_date_in = MapCompose(remove_tags, date_value_extractor
                                 , remove_commas)
