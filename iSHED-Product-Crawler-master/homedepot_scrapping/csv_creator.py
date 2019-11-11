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
        fieldnames = ['Item #', 'Model #', 'Item Name', 'Description', 'Product Details', 'Price (New/Used)', 'Highlights/Features', 'Average',
                      'Pictures', 'Specifications', 'Manual / Guides']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()

        writer.writerows([{"Item #": data['product_id'], "Model #": data['model_number'], 'Item Name': data['product_title'], 'Description': data['product_description'],
                           'Product Details': data['product_descriptive'], 'Price (New/Used)': data['price'], 'Highlights/Features': data['product_highlights'],
                           'Average': data['average_rating'], 'Pictures': data['product_images'],
                           'Specifications': data['product_sepcifications'], 'Manual / Guides': data['product_manuals']}])
        print("Writing complete")