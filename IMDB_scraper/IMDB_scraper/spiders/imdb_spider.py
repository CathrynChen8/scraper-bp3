# https://www.imdb.com/title/tt0120737/
# to run
# scrapy crawl imdb_spider -o movies.csv

import scrapy

class ImdbSpider(scrapy.Spider):
    name = 'imdb_spider'
    
    start_urls = ['https://www.imdb.com/title/tt0120737/']

    def parse(self, response):
        cast_page = response.urljoin("fullcredits")
        
        yield scrapy.Request(cast_page, callback = self.parse_full_credits)
        
    def parse_full_credits(self, response):
        actors = [a.attrib["href"] for a in response.css("td.primary_photo a")]

        for actor in actors:
    
            actor_urls = response.urljoin(actor)
            yield scrapy.Request(actor_urls, callback = self.parse_actor_page)
            
    
    def parse_actor_page(self, response):
        movie = response.css("b a::text").getall()
        name = response.css("div span.itemprop::text").get()
        
        
        yield {
            "name" : name,
            "movie": movie }
    
        
    
