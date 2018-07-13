# YouTube Scraper with Scrapy
-------------------------------

# NOTE: This scraper is only meant for educational use. For commercial utilization, Please use Youtube API.

## Description
Web Scraping has its major value in data mining and data visualization field. With the global web filled with huge data publicly
available, there is need to extract such data in a presentable way. That's where the data scraping comes in. This repo provides
with a sample web scraper written for a Youtube page in Scrapy. Given a Youtube page, the scraper yields following information:
  
- Video Title
- Views
- Likes
- Dislikes
- Publish Date
- Channel Name
- Channel Subscriber count

After running the scraper, a csv file is generated with all the data. Besides CSV, a text file with extracted Youtube video links is created. The scraper also provides default values to fields that cannot be located on the page on some links.

------------------------------------------

## Usage
Install Python 2.7 and scrapy. Then, download the repo and open the terminal in root folder (with scrapy.cfg and YoutubeScraper folder). For the input, there are following two methods:

1. input.txt
2. command line

For input.txt, add all the urls in the text file. There should only be one url per line. Enter the command "scrapy crawl YoutubeSpider" and all the data
will be extracted and saved to data.csv file. 

For CLI, use command "scrapy crawl YoutubeSpider -a url=ANY_YOUTUBE_URL". This is an example of CLI usage : "scrapy crawl YoutubeSpider -a url=https://www.youtube.com/watch?v=yy76z4u6WqE"

The scraper provides login utility to extract links based on query history. For now, the login details need to be hardcoded in the spider file.

#### CLI has high priority than input.txt. In cases where both input methods are available, only CLI input is handled.
