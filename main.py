from lxml import html
import requests
from pprint import pprint
from pymongo import MongoClient
from pymongo import errors

url = 'https://news.mail.ru/?_ga=2.124390282.1447867404.1643808979-1082915779.1623679780'
params = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/98.0.4758.82 Safari/537.36'}
response = requests.post(url, params=params)
dom = html.fromstring(response.text)
news_link = dom.xpath('//div[contains(@class, "daynews__item")]//a/@href | //ul/li//a/@href')

client = MongoClient('127.0.0.1', 27017)
db = client['news']
news_items = db.news

for new in news_link:
    response = requests.post(new, params=params)
    dom = html.fromstring(response.text)
    news_list = ({'_id': new.split('ru/')[1],
                 'источник': dom.xpath('//a[contains(@class, "breadcrumbs__link")]/span/text()')[0],
                  'наименование': dom.xpath('//div[@class="hdr__wrapper"]/span/h1/text()')[0],
                  'ссылка': new,
                  'дата публикации': ((dom.xpath('//span[@datetime]/@datetime')[0]).replace('T', ' ')).split('+')[0]})
    try:
        news_items.insert_one(news_list)
    except errors.DuplicateKeyError:
        continue
for new in news_items.find({}):
    pprint(new)
