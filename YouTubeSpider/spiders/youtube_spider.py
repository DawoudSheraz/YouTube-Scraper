import scrapy
import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from YouTubeSpider.items import YouTubeDataModel
from YouTubeSpider.items import YoutubeItemLoader


class YoutubeSpider(CrawlSpider):

    """
    Youtube Spider class that extracts data from a valid Youtube link
    """

    links_out_file = open('%s.txt' % datetime.datetime.now(), 'w')
    unique_links = {}   # To avoid duplicate links in link extractor
    name = "YoutubeSpider"
    domain = ["youtube.com"]

    def start_requests(self):
        """
        Reads url from input.csv and generates request for each one of them
        :return: Request for each url
        """
        input_file = open('input.txt', 'r')
        start_url = []

        # Check for command line input
        try:
            start_url = [self.url]
        except AttributeError:
            # If no CL argument, read links from txt file
            start_url = [link for link in input_file]

        # Generating request for every url
        for url in start_url:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """
        To parse the response and extract the required mentioned fields
        :param response: Page from the given url
        :return: data dictionary containing the extracted data
        """
        # with open("tem.html", 'w') as f:
        #     f.write(response.body)

        # Parse the links
        self.parse_links(response)

        yt_item_loader = YoutubeItemLoader(YouTubeDataModel())
        yt_item_loader.add_value('url', response.url)
        yt_item_loader.add_value('title', self.get_video_title(response))
        yt_item_loader.add_value('views', self.get_video_views(response))
        yt_item_loader.add_value('likes', self.get_video_likes(response))
        yt_item_loader.add_value('dislikes', self.get_video_dislikes(response))
        yt_item_loader.add_value('channel_name', self.get_video_channel_name(response))
        yt_item_loader.add_value('channel_subscriber_count', self.get_subscriber_count(response))
        yt_item_loader.add_value('publish_date', self.get_video_publishing_date(response))

        return yt_item_loader.load_item()

    def get_video_title(self, response):
        """
        Returns the Youtube page title, empty is not found.

        :param response: Fetched Page
        :return: title of page, empty if invalid entry
        """
        return response.css(".watch-title::text").extract_first(default='')

    def get_video_views(self, response):
        """
        Returns the number of views for a given YouTube url.
        :param response: Fetched Page
        :return: number of views, empty if not found
        """
        return response.css(".watch-view-count::text")\
            .extract_first(default='')

    def get_video_likes(self, response):
        """
        Returns number of likes for a given Youtube url.
        :param response: Fetched Page
        :return: number of likes, empty if invalid
        """
        return response.css(".like-button-renderer-like-button")\
            .extract_first(default='')

    def get_video_dislikes(self, response):
        """
        Returns number of dislikes for a given Youtube url.
        :param response: Fetched Page
        :return: number of dislikes, empty if invalid
        """
        return response.css(".like-button-renderer-dislike-button")\
            .extract_first(default='')

    def get_video_channel_name(self, response):
        """
        Returns the channel name from which youtube video was published.

        :param response: Fetched Page
        :return: Channel name, empty if Invalid or not found
        """
        return response.css("div.yt-user-info")\
            .extract_first(default='')

    def get_subscriber_count(self, response):
        """
        Returns the number of subscribers of channel.

        :param response: Fetched Page
        :return: Subscriber count, empty if not found
        """
        return response.css('.yt-subscriber-count')\
            .extract_first(default='')

    def get_video_publishing_date(self, response):
        """
        Returns the publishing date for a Youtube video

        :param response: Fetched Page
        :return: Publishing Date, empty if not found
        """
        return response.css(".watch-time-text").extract_first(default='')

    def parse_links(self, response):
        """
        Given a response object, valid Youtube videos links are extracted.

        The function extracts all urls and check for validity using
        1. watch?v string
        2. allowed domain
        The valid urls are then saved to csv
        :param response: fetched page
        :return:
        """

        urls = LinkExtractor(canonicalize=True, allow_domains=self.domain)\
            .extract_links(response)

        for link in urls:
            # If link was already extracted on another page, don't save it
            if link.url in self.unique_links:
                continue
            if 'watch?v' in link.url:
                self.links_out_file.write('%s\n' % link.url)
                self.unique_links[link.url] = 1





