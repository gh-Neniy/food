from curl_cffi import requests
from Details.Delay import Delay

import time
import sys

API = 'https://5d.5ka.ru/api/'
CATALOG = 'catalog/v3/stores/5076/categories?mode=delivery&include_subcategories=1&include_restrict=true'
PRODUCTS1 = 'catalog/v2/stores/5076/categories/'
PRODUCTS2 = '/products?mode=delivery&include_restrict=true&limit=499&offset='

def ProductsQuery(category: str, offset: str) -> str:
  return API + PRODUCTS1 + category + PRODUCTS2 + offset


def SendRequest(session: requests.Session, query: str) -> dict:
  response = session.get(query)

  count = 0
  while 500 <= response.status_code <= 599 and count < 3:
    print(f"Error on server with code {response.status_code}, retry")
    time.sleep(Delay())
    response = session.get(query)
    count += 1

  if response.status_code != 200:
    print(response.text)
    print('Error on getting catalog with code', response.status_code)
    sys.exit(1)

  return response.json()


TARGET_CATEGORIES = [
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

def GetCategories(session: requests.Session) -> list[dict]:
  categories = SendRequest(session, API + CATALOG)
  return [category for category in categories if category['name'] in TARGET_CATEGORIES]


def ProductsRequest(session: requests.Session, category: dict, offset: str = '0'):
  products = SendRequest(session, ProductsQuery(category['id'], offset))
  return products['products']


# API restriction: offset + limit <= 1000
def GetProducts(session: requests.Session, categories: list[dict]) -> list[str]:
  result = []
  for category in categories:
    time.sleep(Delay())
    products = ProductsRequest(session, category)
    if len(products) == 499:
      time.sleep(Delay())
      products += ProductsRequest(session, category, '499')

    print('Got', len(products), 'on category', category['name'])
    result += [str(product['plu']) for product in products]

  return list(set(result))


PRODUCT1 = 'catalog/v2/stores/5076/products/'
PRODUCT2 = '?mode=delivery&include_restrict=true'

def GetProduct(session: requests.Session, product_id: str) -> dict:
  query = API + PRODUCT1 + product_id + PRODUCT2
  return SendRequest(session, query)
