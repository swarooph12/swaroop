import csv
import os
import os.path
import io
import datetime
today_date = datetime.date.today()


def product_csv_creator_file(data, category_name):

    if not os.path.exists('product_csv/'+str(today_date)+'/'):
        os.makedirs('product_csv/'+str(today_date)+'/')
    filename = 'product_csv/'+str(today_date)+'/'+category_name+'.csv'
    file_exists = os.path.isfile(filename)
    with io.open(filename, 'a', encoding='utf-8') as csvfile:
        fieldnames = ['Sub-category' ,'price','image','rating','details','cutomer-reivewcount']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()

        writer.writerows([{'Sub-category':data['name'] ,'price':data['price'],
                           'image':data['img-url'],'rating':data['star-rating'],
                           'details':data['details'],'cutomer-reivewcount':data['customer-reviews-count']}])
                           
        print("Writing complete")