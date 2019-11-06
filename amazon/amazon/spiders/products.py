# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor



class ProductsSpider(scrapy.Spider):
    name = 'products'
    allowed_domains = ['www.amazon.com/']
    start_urls = ['https://www.amazon.com/s?k=vivitar+lens+model+mc&ref=nb_sb_noss',
                  'https://www.amazon.com/s?k=lawn+mower+american+push+mower&ref=nb_sb_noss_2',
                  'https://www.amazon.com/s?k=lens+samyang+macro+slr+interchangeable&ref=nb_sb_noss'
    ]


    rules = (
        Rule(LinkExtractor(allow=(), restrict_css=('.pageNextPrev',)),
             callback="parse_item",
             follow=True),)

    def parse_item(self, response):
        item_links=response.css('.rush-component> .a-link-normal::attr(href)').extract()
        for a in item_links:
            yield scrapy.Request(a , callback=self.parse_detail_page)
        print('Processing..' + response.url)

    
