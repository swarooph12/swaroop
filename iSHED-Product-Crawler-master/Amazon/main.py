from urllib import request
import urllib.parse
import urllib.error
from bs4 import BeautifulSoup
import ssl
import json
Asin =[]
import requests
from lxml import html  
import csv,os,json
import requests
import re
from time import sleep
import pandas as pd
import random
import csv_creator
from fake_useragent import UserAgent

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def get_asin(product_name):
    category_name = product_name
#     category_name = category_name.strip(' ')
    try:
#         new_data = pd.DataFrame()
        url = 'https://www.amazon.in/s?k=' + category_name + '&ref=nb_sb_noss'
        #https://www.amazon.in/s?k=hammers
        print(url)
        ua = UserAgent()
        header  = {'User-Agent':str(ua)}
        #header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:63.0) Gecko/20100101 Firefox/63.0'}
        # a = random.choice(user_agent_list)
        page = requests.get(url, headers=header).content
        page = page.decode('utf-8')
        #print(page)

        pattern = re.compile(r"/dp/(?P<asin>\w+).*")
        asin =  re.findall(pattern,page)
        
        print(len(asin))
        asin =asin[1:]
        print(len(asin))
        for i in asin:
            print(i)
            scrape_data(i,category_name)
            print(asin)
#         return asin
#         Asin.append(asin)

    except Exception as e:
        print(e)
        pass
		
def scrape_data(asin,category_name):
    category_name = category_name
    print(category_name)
    url = 'http://www.amazon.in/dp/' +str(asin)
    print(url)
    html = urllib.request.urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, 'html.parser')
    html = soup.prettify('utf-8')
    product_json = {}
    for divs in soup.findAll('div', attrs={'class': 'a-box-group'}):
        try:
            product_json['brand'] = divs['data-brand']
            break
        except:
            pass
    for spans in soup.findAll('span', attrs={'id': 'productTitle'}):
        name_of_product = spans.text.strip()
        product_json['name'] = name_of_product
        break
    for divs in soup.findAll('div'):
        try:
            price = str(divs['data-asin-price'])
            product_json['price'] = '$' + price
            break
        except:
            pass
    # This block of code will help extract the image of the item in dollars

    for divs in soup.findAll('div', attrs={'id': 'rwImages_hidden'}):
        for img_tag in divs.findAll('img', attrs={'style': 'display:none;'
                                    }):
            product_json['img-url'] = img_tag['src']
            break
    # This block of code will help extract the average star rating of the product
    for i_tags in soup.findAll('i',
                               attrs={'data-hook': 'average-star-rating'}):
        for spans in i_tags.findAll('span', attrs={'class': 'a-icon-alt'}):
            product_json['star-rating'] = spans.text.strip()
            break
    product_json['details'] = []
    for ul_tags in soup.findAll('ul',
                                attrs={'class': 'a-unordered-list a-vertical a-spacing-none'
                                }):
        for li_tags in ul_tags.findAll('li'):
            for spans in li_tags.findAll('span',
                    attrs={'class': 'a-list-item'}, text=True,
                    recursive=False):
                product_json['details'].append(spans.text.strip())
                    
    for spans in soup.findAll('span', attrs={'id': 'acrCustomerReviewText'
                              }):
        if spans.text:
            review_count = spans.text.strip()
            product_json['customer-reviews-count'] = review_count
            break
    csv_creator.product_csv_creator_file(product_json, category_name)
get_asin('TV')
    
    		
