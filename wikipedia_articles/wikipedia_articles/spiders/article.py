import scrapy
from wikipedia_articles.items import articles


class ArticleSpider(scrapy.Spider):
    name = 'article'
    allowed_domains = ['en.wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/Wikipedia:Featured_articles']

    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'file:C://Users//sebas//PycharmProjects//web-scrapping//wikipedia_articles//featured_article-%(time)s.json'
    }

    def parseFirst(self, response):
        host = self.allowed_domains[0]

        t = response.xpath('//h1[@id="firstHeading"]/text()').extract()
        p = response.xpath('//div[@class="mw-parser-output"]/p[2]').extract()
        #p = response.css('.mw-parser-output > p::text').extract()

        article = {
            'link': response.url,
            'body': {
                'title': t[0],
                'paragraph': p[0]
            }
        }
        print(t)
        yield article


    def parse(self, response):
        host = self.allowed_domains[0]
        count = 0

        for link in response.css(".featured_article_metadata > a"):
            if count < 25:
                count = count + 1

                next_page_url = f"http://{host}{link.attrib.get('href')}"
                if next_page_url:
                    yield scrapy.Request(url=next_page_url, callback=self.parseFirst)
