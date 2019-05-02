import scrapy
import csv
import pandas as pd


'''
Open a terminal/command at the location of the scraper 'CentralAfricanRepublicScraper'
in your terminal run the following script

'scrapy crawl News_Scraper -o NewsScraperReuters.csv -t csv' - this will save a csv in your file directory

syntax: scrapy crawl SCRAPER_NAME -output FILENAME.csv -t csv
'''

class NewsScraper(scrapy.Spider):
    name = 'News_Scraper'  #name of the scraper - to call in terminal/command
    allows_domains = ['http://feeds.reuters.com/reuters/']  #starting domain

    output = 'ReutersAfrica_TopStoriesRSSFeed_List.csv'  #csv output when script is run - list of lists

    def __init__(self):
        open(self.output, 'a').close()


    def start_requests(self): # list of all the URLs we're going to scrape
        yield scrapy.Request('http://feeds.reuters.com/reuters/AFRICATopNews', self.parse)
        yield scrapy.Request('http://feeds.reuters.com/reuters/AFRICAcentralAfricanRepublicNews', self.parse)
        yield scrapy.Request('http://feeds.reuters.com/reuters/AFRICAdrcNews', self.parse)
        yield scrapy.Request('http://feeds.reuters.com/reuters/AFRICAlibyaNews', self.parse)
        yield scrapy.Request('http://feeds.reuters.com/reuters/AFRICAmozambiqueNews', self.parse)
        yield scrapy.Request('http://feeds.reuters.com/reuters/AFRICAsomaliaNews', self.parse)
        yield scrapy.Request('http://feeds.reuters.com/reuters/AFRICAegyptNews', self.parse)
        yield scrapy.Request('http://feeds.reuters.com/reuters/AFRICAcongoNews', self.parse)

    def parse(self, response):
        with open(self.output, 'a', newline ='') as f:
            writer = csv.writer(f)
            for article in response.xpath("//item"):
                title = article.xpath("title/text()").extract()
                content = article.xpath("description/text()").extract()
                date = article.xpath("pubDate/text()").extract()
                link = article.xpath("link/text()").extract()
                country = article.xpath('//title/text()').extract_first()  #country selected for RSS feed
                writer.writerow([title, content, date, country, link])
                yield{'Title': title, 'Content': content, 'Date': date, 'Country': country, 'Link': link}





# df = pd.read_csv('/Users/jkuypers/Documents/NOVA_IMS/Term_2/Text_Mining/FinalProject/CentralAfricanRepublicScraper/ReutersAfricaRssSelected.csv')
# df