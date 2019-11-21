# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GreentopItem(scrapy.Item):
    
    # define the fields for your item here like:
    Product_Name = scrapy.Field()
    Product_ID =scrapy.Field()
    Product_Model=scrapy.Field()
    Product_Brand = scrapy.Field()
    Rating = scrapy.Field()
    Description = scrapy.Field()
    Image_urls = scrapy.Field()
    Images = scrapy.Field()
    Price = scrapy.Field()
    Features= scrapy.Field()
    
    
    
