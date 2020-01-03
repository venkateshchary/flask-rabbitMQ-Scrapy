import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.item import Item, Field
import hashlib 
from producer import producer



class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        title = response.css('title::text').get()
        text = response.css('span.text::text').get()
        author = response.css('small.author::text').get()
        print("author ->",author)
        tags = response.css('div.tags a.tag::text').getall()
        d={"title":title,"text":text,"author":author,"tags":tags}
        if len(text)>0:
            h_text = text[:10]
            print("h_text ->",h_text)
            print("author ->",author)
            str = h_text+author
            hash_object = hashlib.sha1(str.encode())
            result = hash_object.hexdigest()
            d["hash"] = result
        else:
            d["hash"] = 0
        producer(msg=d)


# if __name__ =="__main__":
#     process = CrawlerProcess()
#     process.crawl(QuotesSpider)
#     process.start() 