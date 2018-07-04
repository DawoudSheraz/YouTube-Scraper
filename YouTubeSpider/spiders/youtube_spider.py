import scrapy
from YouTubeSpider.items import YouTubeDataModel


class YoutubeSpider(scrapy.Spider):

    """
    Youtube Spider class that extracts data from a valid Youtube link
    """

    name = "YoutubeSpider"
    domain = ["youtube.com"]

    def start_requests(self):
        """
        Reads url from input.csv and generates request for each one of them
        :return: Request for each url
        """
        input_file = open('input.txt','r')
        start_url = []
        for each in input_file:
            start_url.append(each)
        for url in start_url:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """
        To parse the response and extract the required mentioned fields
        :param response: Page from the given url
        :return: data dictionary containing the extracted data
        """
        with open("tem.html", 'w') as f:
            f.write(response.body)

        youtube_item = YouTubeDataModel()
        youtube_item['url'] = response.url
        youtube_item['title'] = self.get_video_title(response)
        youtube_item['views'] = self.get_video_views(response)
        youtube_item['likes'] = self.get_video_likes(response)
        youtube_item['dislikes'] = self.get_video_dislikes(response)
        youtube_item['channel_name'] = self.get_video_channel_name(response)
        youtube_item['channel_subscriber_count'] = self.get_subscriber_count(response)
        youtube_item['publish_date'] = self.get_video_publishing_date(response)

        return youtube_item

    def get_video_title(self, response):
        """
        Returns the Youtube page title, empty is not found.

        :param response: Fetched Page
        :return: title of page, empty if invalid entry
        """
        title = ""
        try:
            title = response.css(".watch-title::text").extract_first()
            title = title.strip()
        except ValueError:
            pass
        return title

    def get_video_views(self, response):
        """
        Returns the number of views for a given YouTube url.
        :param response: Fetched Page
        :return: number of views, empty if not found
        """
        views = ""
        try:
            views = response.css(".watch-view-count::text").extract_first()
            views = views.split()[0]
        except ValueError:
            pass
        return views

    def get_video_likes(self, response):
        """
        Returns number of likes for a given Youtube url.
        :param response: Fetched Page
        :return: number of likes, empty if invalid
        """
        likes = ""
        try:    # First get the like button, and then data from child span
            likes = response.css(".like-button-renderer-like-button")\
                .css(".yt-uix-button-content::text")\
                .extract_first()
        except ValueError:
            pass
        return likes

    def get_video_dislikes(self, response):
        """
        Returns number of dislikes for a given Youtube url.
        :param response: Fetched Page
        :return: number of dislikes, empty if invalid
        """
        dislikes = ""
        try:  # First get the dislike button, and then data from child span
            dislikes = response.css(".like-button-renderer-dislike-button") \
                .css(".yt-uix-button-content::text") \
                .extract_first()
        except ValueError:
            pass
        return dislikes

    def get_video_channel_name(self, response):
        """
        Returns the channel name from which youtube video was published.

        :param response: Fetched Page
        :return: Channel name, empty if Invalid or not found
        """
        channel_name = ""
        try:        # Get div containing channel name, and then data from child
            channel_name = response.css("div.yt-user-info")\
                .css('a.yt-uix-sessionlink.spf-link::text')\
                .extract_first()
        except ValueError:
            pass
        return channel_name

    def get_subscriber_count(self, response):
        """
        Returns the number of subscribers of channel.

        :param response: Fetched Page
        :return: Subscriber count, empty if not found
        """
        channel_subscriber_count = ""
        try:
            channel_subscriber_count = response.css('.yt-subscriber-count::text')\
                                    .extract_first()
        except ValueError:
            pass
        return channel_subscriber_count

    def get_video_publishing_date(self, response):
        """
        Returns the publishing date for a Youtube video

        :param response: Fetched Page
        :return: Publishing Date, empty if not found
        """
        publish_date = ""

        try:
            publish_date = response.css(".watch-time-text::text")\
                .extract_first().split()[2:]        # Process extracted string to get date list
            publish_date = " ".join(publish_date)   # Join date list into string
        except ValueError:
            pass
        return publish_date



