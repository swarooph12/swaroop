import time
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
# product_detals = {}


def Scrape(url,Category,sub_name):
    time.sleep(2)
    url = url
    Category=Category
    print(Category)
    ua = UserAgent()
    header  = {'User-Agent':str(ua)}
#     result = requests.get(url)
    result=requests.get(url,headers = header, timeout = 20)
    soap = BeautifulSoup(result.content , 'lxml')
    product_detals = {}
    for i in soap.find_all('div',{'class':'product-detail-wrapper'}):
        try:
            product_detals['Name'] = i.find('h1').text
        except:
            product_detals['Name']='Nill'
    try:        
        product_detals['Price'] = i.find(class_ = 'regular-price').text.strip()
    except:
        product_detals['Price'] ='Nill'
#     Sku = soap.find('div',{'class':'product-sku'}).text.strip()
    
    try:
        model = soap.find_all('div',{'class':'accordion-body-content'})
        product_detals['Model_number']= model[-3].find('li').text.strip()
    except :
        product_detals['Model_number'] ='Nill'
    try:
        
        product_detals['Description']=soap.find('p',{'class':'product-short-description'}).text.strip()
    except :
        product_detals['Description'] = 'Nill'
    try:
        product_detals['Category']=Category
    except:
        product_detals['Category'] ='Nill'
    try:
        product_detals['Image']=soap.find('img',{'class':'viewer-main-image'}).get('srcset').strip('//')
    except:
        product_detals['Image'] ='Nill'
    print(product_detals)
    product_csv_creator_file(product_detals, sub_name)

import csv
import os
import os.path
import io
import datetime
today_date = datetime.date.today()
def product_csv_creator_file(data, category_name):
    
    if not os.path.exists('product_csv/'+str(today_date)+'/'):
        
        
        os.makedirs('product_csv/'+str(today_date)+'/')
        filename = 'product_csv/'+str(today_date)+'/'+ category_name +'.csv'
        file_exists = os.path.isfile(filename)
        with io.open(filename, 'a', encoding='utf-8') as csvfile:
            
            fieldnames = ['Category','Sub-category' ,'price','Image','Model_number','Description']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()

            writer.writerows([{'Category':data['Category'],'Sub-category':data['Name'] ,'price':data['Price'],
                               'Image':data['Image'],'Model_number':data['Model_number'],
                               'Description':data['Description']}])
                               
            print("Writing complete")



def Search_url(Category,name):
    sub_name = name
    Category = Category
    print(sub_name)
    url ='https://www.biglots.com/search/?Ntt='+ str(sub_name)
    base_url = 'https://www.biglots.com'
    print(url)
    page_response = requests.get(url,timeout=10)
    bs = BeautifulSoup(page_response.content, 'lxml')    
    links=[]
    for link in bs.find_all('a',{'class':'product-link'}):
        
        
    #   print(link.get('href'))
        links.append(link.get('href'))
        for link in links:
            complete = base_url+link
            print(complete)
            Scrape(complete,Category,sub_name)
            time.sleep(2)
Search_url('Outdoor and Fun','Chairs')            


                    











    
