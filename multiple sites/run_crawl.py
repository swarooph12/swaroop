Python 2.7.17 (v2.7.17:c2f86d86e6, Oct 19 2019, 21:01:17) [MSC v.1500 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
>>> import scrapy

class MySpider(scrapy.Spider):

    name = 'myspider'

    #allowed_domains = ['http://www.ikea.com']

    start_urls = ['http://www.ikea.com/ae/en/catalog/categories/departments/childrens_ikea/31772/']

    def parse(self, response):
        print('url:', response.url)

        all_products = response.css('div.product')

        for product in all_products:
            title = product.css('div.productTitle.floatLeft ::text').extract()
            description = product.css('div.productDesp ::text').extract()
            price = product.css('div.price.regularPrice ::text').extract()
            price = price[0].strip()

            print('item:', title, description, price)

            yield {'title': title, 'description': description, 'price': price}

# --- it runs without project and saves in 'output.csv' ---

from scrapy.crawler import CrawlerProcess

c = CrawlerProcess({
    'USER_AGENT': 'Mozilla/5.0',
    'FEED_FORMAT': 'csv',
    'FEED_URI': 'output.csv',
})
c.crawl(MySpider)
c.start()
