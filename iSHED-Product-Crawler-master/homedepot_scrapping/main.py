import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import csv_creator


def search_category(url_check, category_name, pagination_url):
    ua = UserAgent()
    header = {'User-Agent': str(ua.random)}
    category_name = category_name.replace("/", " ")
    if url_check == 'pagination':
        url = pagination_url
    else:
        url = 'https://www.homedepot.com/s/' + category_name
    result = requests.get(url, headers=header).content
    soup = BeautifulSoup(result, 'html.parser')
    base_url = 'https://www.homedepot.com'
    product_div = soup.find_all('div', class_='plp-pod--default')

    if not product_div:
        #print('div_empty')
        product_div = soup.find_all('div', class_='product-pod__col')

    for single_product_div in product_div:
        image_div = single_product_div.find('a', attrs={'data-podaction': 'product image'})
        anchor_tag = image_div

        if image_div is None:
            #print('image_empty')
            image_div = single_product_div.find('div', class_='product-pod')
            anchor_tag = image_div.find('a')

        print(base_url + anchor_tag['href'])
        get_single_product(base_url + anchor_tag['href'], category_name)

    pagination_div = soup.find('a', attrs={'title': 'Next'})
    if pagination_div is not None:
        pagination_url = base_url + pagination_div.get('href')
        print('Next Url :' + pagination_url)
        search_category('pagination', category_name, pagination_url)


def get_single_product(url, category_name):
    product_details = {}
    ua = UserAgent()
    header = {'User-Agent': str(ua)}
    product_details['product_id'] = url.split('/')[-1]
    ajax_url = 'https://www.homedepot.com/p/svcs/frontEndModel/' + product_details['product_id']
    page_response = requests.get(ajax_url, headers=header).json()

    product_details['model_number'] = page_response['primaryItemData']['info']['modelNumber']
    product_details['product_title'] = page_response['primaryItemData']['info']['productLabel']
    product_details['product_description'] = page_response['primaryItemData']['info']['description']
    product_price = page_response['primaryItemData']['itemExtension']['pricing']
    product_details['average_rating'] = page_response['primaryItemData']['ratingsReviews']['averageRating']
    product_details['price'] = str(product_price['specialPrice']) + ' / ' + str(product_price['originalPrice'])

    product_image_list = []
    if 'media' in page_response['primaryItemData']:
        for images in page_response['primaryItemData']['media']['mediaList']:
            if 'video' in images:
                print("Video")
            elif 'height' in images and images['height'] == '1000':
                product_image_list.append(images['location'])
        product_details['product_images'] = ','.join(product_image_list)
    else:
        product_details['product_images'] = 'Not found'

    product_specification_list = []
    product_highlights_list = []
    product_manual_list = []
    product_descriptive_list = []
    if 'attributeGroups' in page_response['primaryItemData']:
        for specification in page_response['primaryItemData']['attributeGroups']:
            if specification['groupType'] == 'functional details' or specification['groupType'] == 'supplemental dimensions' or specification['groupType'] == 'base dimensions':
                for specifications in specification['entries']:
                    product_specification_list.append(specifications['name'] + " : " + specifications['value'])
            elif specification['groupType'] == 'descriptive':
                for descriptive in specification['entries']:
                    product_descriptive_list.append(descriptive['name'] + " : " + descriptive['value'])
            elif specification['groupType'] == 'product highlights':
                for highlights in specification['entries']:
                    product_highlights_list.append(highlights['name'] + " : " + highlights['value'])
            elif specification['groupType'] == 'pdf documents':
                for manuals in specification['entries']:
                    product_manual_list.append(manuals['name'] + " : " + manuals['url'])

        product_details['product_sepcifications'] = ','.join(product_specification_list)
        product_details['product_highlights'] = ','.join(product_highlights_list)
        product_details['product_manuals'] = ','.join(product_manual_list)
        product_details['product_descriptive'] = ','.join(product_descriptive_list)
    else:
        product_details['product_sepcifications'] = 'Not found'
        product_details['product_highlights'] = 'Not found'
        product_details['product_manuals'] = 'Not found'
        product_details['product_descriptive'] = 'Not found'

    print(product_details)

    csv_creator.product_csv_creator_file(product_details, category_name)

#get_data_from_new_url('https://www.homedepot.com/p/Whirlpool-25-cu-ft-French-Door-Refrigerator-in-Fingerprint-Resistant-Stainless-Steel-WRX735SDHZ/301859152')
#get_single_product('https://www.homedepot.com/p/Whirlpool-25-cu-ft-French-Door-Refrigerator-in-Fingerprint-Resistant-Stainless-Steel-WRX735SDHZ/301859152')
search_category('category_name', 'Hand Tools - Clamp and Vise', '')
