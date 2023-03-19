import sys

from scrapy.exceptions import CloseSpider
import re
from datetime import datetime
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings






class PostsSpider(scrapy.Spider):

    if len(sys.argv) > 2:
        arg1 = sys.argv[0]
        names = sys.argv[1]
        max = sys.argv[2]
        runtime = sys.argv[3]

    page_number = 0
    name = 'posts'
    allowed_domains = ['ra.co']


    # global artist
    # artist = input('Artist name:')
    start_urls = [
        f'https://ra.co/dj/janeret/past-events?'
    ]

    custom_settings = {'AUTOTHROTTLE_ENABLED': True,
                       'AUTOTHROTTLE_MAX_DELAY': 120,
                       'AUTOTHROTTLE_START_DELAY': 10,
                       'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.22',
                    }


    def parse(self, response):

        if len(response.css('li.Column-sc-18hsrnn-0.inVJeD')) == 0:
            raise CloseSpider('No more events')

        for link in response.css('li.Column-sc-18hsrnn-0.inVJeD div h3 a::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_act)

        next_page = f'https://ra.co/dj/janeret/past-events?page={str(PostsSpider.page_number)}'


        PostsSpider.page_number += 1
        if PostsSpider.page_number == 3:
            raise CloseSpider('No more events')
        print(PostsSpider.page_number)
        yield response.follow(next_page, callback=self.parse)

    def parse_act(self, response):
        date = response.xpath('//*[@id="__next"]/div[2]/header/div/div[2]//div/ul/li[2]/div/div[2]/a/span/text()').get()
        event = response.xpath('//*[@id="__next"]/div[2]/header/div//div/div/div[2]/h1/span/text()').get()
        promotors = response.xpath('//*[@id="__next"]/div[2]/header/div/div[2]/div[2]/div/ul/li[3]/div/div[2]/a/span/text()').getall()
        location = response.xpath('//*[@id="__next"]/div[2]/header/div//div[1]/div/div/div[1]/nav/ul/li[1]/div/a/span/text()').get()
        country = response.xpath('//*[@id="__next"]/div[2]/header/div//div[1]/div/div/div[1]/nav/ul/li[1]/div/a').attrib['href']
        venue = response.xpath('//*[@id="__next"]/div[2]/header/div/div[2]//div/ul/li[1]/div//span/text()')[1].get()
        acts = response.xpath('//*[@id="__next"]/div[2]/section[1]/div/section[1]/div/div/div[2]/ul/li[1]/div/span/a/span/text()').getall()

        date = re.sub(r'^.*?, ', '', date)

        promotors = ', '.join(promotors)

        if len(date) == 4:
            date = f'99-99-{date}'

        elif len(date) >= 15:
            date = date[5:]

        elif date[-4: -2] == '20':
            date = datetime.strptime(date, '%b %d, %Y').strftime('%d-%m-%Y')
        else:
            date = datetime.strptime(date, '%d %b').strftime('%d-%m') + '-2023'

        country = country.split('/')[-2].upper()

        acts = ', '.join(acts)

        item = {
            'date': date,
            'Event': event,
            'promotors': promotors,
            'Location': location,
            'Country': country,
            'Venue': venue,
            'Acts': acts
        }

        yield item


if __name__== '__main__':
    process = CrawlerProcess()
    process.crawl(PostsSpider)
    process.start()