# -*- coding: utf-8 -*-
import scrapy
from ..items import GreentopItem


class GreenTopSpider(scrapy.Spider):
    name = 'green_top'

    #how many pages you want to scrape
    no_of_pages= 6
    # Headers to fix 503 service unavailable error
    # Spoof headers to force servers to think that request coming from browser ;)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.2840.71 Safari/539.36'}
    allowed_domains = ['greentophuntfish.com']
    start_urls = ['http://www.greentophuntfish.com/']

    def start_requests(self):
        # starting urls for scraping
        urls = ["https://www.greentophuntfish.com/hunting/knives-tools/knife-sharpeners/?page=%s" % page for page in range(1,3)]
               #['http://example.com/foo/bar/page_%s' % page for page in xrange(1,54)]

        for url in urls: yield scrapy.Request(url = url, callback = self.parse, headers = self.headers)

 

    def parse(self, response):
        
        
        self.no_of_pages -= 1
        # print(response.text)

        greentop_res =response.xpath("//h4[@class='card-title']/a").xpath("@href").getall()
        
        # print(len(greentop_res))

        for green in greentop_res:
            final_url = response.urljoin(green)
            yield scrapy.Request(url=final_url, callback = self.parse_greentop, headers = self.headers)
            # break
            # print(final_url)

        # print(response.body)
        # title = response.xpath("//span[@class='a-size-medium a-color-base a-text-normal']//text()").getall()
        # title = response.css('span').getall()
        # print(title)
        if(self.no_of_pages > 0):
            
            next_page_url = response.xpath("//a[@class='pagination-link']").xpath("@href").get()
            final_url = response.urljoin(next_page_url)
            yield scrapy.Request(url = final_url, callback = self.parse, headers = self.headers)
            
    def parse_greentop(self, response):
        
        Product_Name = response.xpath("//h4[@class='card-title']/a//text()").get()
        Product_ID =response.xpath("//div[@class='card-figcaption-body']/a").xpath("@data-product-id").get()
        Product_Model ='NA'
        Product_Brand = response.xpath("//p[@class='card-text']//text()").get() or "NA"
        Rating = 'NA'

        Price =  response.xpath("//span[@class='price price--withoutTax']//text()").get()
        print(Price)
        #if len(Price) > 1: Price = Price[1].get()
        #elif len(Price) == 1: Price = Price[0].get()
        #else : Price = Price.get()

        Features= response.xpath("//div[@class='tab-content is-active']/ul").get() or "NA"
        #instock = response.xpath("//div[@id='availability']").xpath("//span[@class='a-size-medium a-color-success']//text()").get() or "Out Stock"
        #instock = instock.strip() == "In stock."
        #reviews = response.xpath("//div[@class='a-expander-content reviewText review-text-content a-expander-partial-collapse-content']/span//text()").getall()
        description_raw = response.xpath("//div[@class='tab-content is-active']").get()

        Img_url = response.xpath("//div[@class='productView-img-container']/a").xpath("@href").get()

        #Description = []
        #for description_temp in description_raw:
            
            #Description.append(description_temp.strip())

        print(Product_Name,Product_ID,Product_Model,Product_Brand,Rating,Img_url)
        # print(final_review)
        # print(reviews)
        # print(description)

        yield GreentopItem(Product_Name = Product_Name,Product_ID = Product_ID,Product_Model =Product_Model,Product_Brand = Product_Brand, Rating = Rating,Price = Price, Features = Features, Description = description_raw, Image_urls = [Img_url])



            
        
