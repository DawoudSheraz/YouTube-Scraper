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

    cookies = {}

    def define_cookies(self, response):

        temp = response.headers.getlist('Set-Cookie')   # Get Cookies List
        # temp = '&&'.join(temp)  # Create String
        # temp = temp.split(';')  # Separate individual value
        # temp = [x for x in temp if '=' in x]    # Only keep cookies having =
        #
        # # Remove cookies having path and domain string
        # temp = [x for x in temp if 'path' not in x]
        # temp = [x for x in temp if 'domain' not in x]
        #
        # # When joined by &&, some cookies without = get joined
        # # This for loop removes such cookies
        # for count in range(0, len(temp)):
        #     if '&&' in temp[count]:
        #         temp[count] = temp[count].split('&&')[1]
        #
        # # Remove all expiry related things
        # temp = [x for x in temp if 'expires' not in x]

        # Every required cookie is in first place of list -
        # - when strings are separated by ';'
        temp = [x.split(';')[0] for x in [j for j in temp]]

        # Create dictionary from list
        for count in range(0, len(temp)):
            val_list = temp[count].split('=')

            # In cases where value actually contains '='
            if len(val_list) >= 3:
                self.cookies[val_list[0]] = '='.join(val_list[1:])
                continue

            self.cookies[val_list[0]] = val_list[1]

    def start_requests(self):
        """
        Reads url from input.csv and generates request for each one of them
        :return: Request for each url
        """
        # First request to Youtube to get user live ID and related cookies
        yield scrapy.Request('https://www.youtube.com/'
                             , callback=self.define_cookies)

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
            yield scrapy.Request(url=url
                                 , callback=self.parse
                                 , cookies=self.cookies)

    def parse(self, response):
        """
        To parse the response and extract the required mentioned fields
        :param response: Page from the given url
        :return: data dictionary containing the extracted data
        """
        with open("tem.html", 'w') as f:
            f.write(response.body)

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





