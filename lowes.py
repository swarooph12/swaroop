import lxml.etree,json
import requests

s = requests.Session()

s.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36'})

resp = s.get('https://www.lowes.com/pd/search/4005755/pricing/2421')

js = lxml.etree.HTML(resp.content).find('./head/script[2]').text
data = js.partition('window.digitalData.products = [')[2].partition('];\n')[0]
product_json = json.loads(data)

print('{},{},{}'.format(product_json["productId"][0], product_json["productName"], product_json["sellingPrice"]))
