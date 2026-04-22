from curl_cffi import requests
from Details.Delay import Delay

import time
import sys


def CategoriesRequest(shop_id: str):
  return 'https://5d.5ka.ru/api/catalog/v3/stores/' + shop_id + '/categories?mode=delivery&include_subcategories=1&include_restrict=true'


def ProductsRequest(shop_id: str, category: str, offset: str) -> str:
  return 'https://5d.5ka.ru/api/catalog/v2/stores/' + shop_id + '/categories/' + category + '/products?mode=delivery&include_restrict=true&limit=499&offset=' + offset


def SendRequest(session: requests.Session, request: str) -> dict:
  response = session.get(request)

  count = 0

  while 500 <= response.status_code <= 599 and count < 3:
    print(f"Error on server with code {response.status_code}, retry")
    time.sleep(Delay())

    response = session.get(request)
    count += 1

  if response.status_code != 200:
    print(response.text)
    print('Error on getting catalog with code', response.status_code)
    sys.exit(1)

  return response.json()


HEALTHY_CATEGORIES = [
  'Готовая еда',
  'Овощи, фрукты, орехи',
  'Молочная продукция и яйцо',
  'Хлеб и выпечка',
  'Мясо, птица, колбасы',
  'Рыба и морепродукты',
  'Бакалея',
  'Замороженные продукты',
  'Вода и напитки',
  'Здоровый выбор'
]

ADDITIONAL_CATEGORIES = [
  'Сладости',
  'Снеки и чипсы'
]


def GetCategories(session: requests.Session, shop_id:str, healthy: bool) -> list[dict]:
  categories = SendRequest(session, CategoriesRequest(shop_id))
  result = [category for category in categories if category['name'] in HEALTHY_CATEGORIES]
  
  if not healthy:
    result += [category for category in categories if category['name'] in ADDITIONAL_CATEGORIES]

  print('Got', len(result), 'categories')

  return result


# API restriction: limit <= 499, offset + limit <= 1000
def GetProducts(session: requests.Session, shop_id: str, categories: list[dict]) -> dict[dict]:
  result = {}

  for category in categories:
    time.sleep(Delay())

    products = SendRequest(session, ProductsRequest(shop_id, category['id'], '0'))['products']
    
    if len(products) == 499:
      time.sleep(Delay())
      products += SendRequest(session, ProductsRequest(shop_id, category['id'], '499'))['products']

    print('Got', len(products), 'on category', category['name'])

    for product in products:
      result[product['plu']] = product

  return result


def ProductRequest(shop_id: str, product_id: int):
  return 'https://5d.5ka.ru/api/catalog/v2/stores/' + shop_id + '/products/' + str(product_id) + '?mode=delivery&include_restrict=true'


def GetProduct(session: requests.Session, shop_id: str, product_id: int) -> dict:
  return SendRequest(session, ProductRequest(shop_id, product_id))
