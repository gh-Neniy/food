from curl_cffi import requests
from contextlib import closing
from Details.Products import GetProduct
from Details.SQLCode import DATABASE_PATH, SELECT, INSERT
from Details.Delay import Delay

import sqlite3
import time
import re

MAX_WORDS_CNT = 7

def Id(product: dict) -> int:
  return product['plu']


def Name(product: dict) -> str:
  words = product['name'].split() # leaves only clear words list, without escape sequences
  result_words = words[:MAX_WORDS_CNT]
  
  if len(words) <= MAX_WORDS_CNT:
    return ' '.join(result_words)
  
  if result_words[-1] in ['с', 'в', 'из', 'и', 'от', 'со'] or result_words[-1].isdigit():
    del result_words[-1]

  result_words.append(words[-1])
  return ' '.join(result_words)


def Price(product: dict) -> float:
  initial_price = product['prices']['regular']

  if product['prices']['discount']:
    initial_price = product['prices']['discount']

  if ''.join(product['property_clarification'].split()).lower() == 'ценаза100г':
    return float(product['min_weight']) * 10 * float(initial_price)
  
  return float(initial_price)


def Ingredients(product: dict) -> str:
  ingredients = product['ingredients']

  if ingredients == None:
    return 'Нет информации'
  
  if all(pattern not in ingredients for pattern in ('.\n\n', '\n\n', '.\n', '. ')): # already one sentence
    return ingredients
  
  # reduce token amount by deleting unnecessary sentences
  ingredients = ingredients.replace('.\n\n', '. ').replace('.\n', '. ').replace('\n\n', '. ')
  sentences = re.sub(r'(\d),\s+(\d)', r'\1,\2', ingredients).split('. ')
  filtered = [sentence for sentence in sentences if all(pattern not in sentence.lower() for pattern in ('предприят', 'может содерж', 'аллергенов'))]

  return '. '.join(filtered)


def UpdateData(session: requests.Session, shop_id: str, products: dict[dict]) -> list[tuple]:
  with closing(sqlite3.connect(DATABASE_PATH)) as database:
    cursor = database.cursor()
    cursor.execute(SELECT)
    id_ingredients = {row[0] : row[1] for row in cursor.fetchall()}

    result = []
    to_update = []

    for id in products.keys():
      if id not in id_ingredients:
        to_update.append(id)
      else:
        result.append((Name(products[id]), id_ingredients[id], Price(products[id])))

    if len(to_update) > 0:
      print(len(to_update), 'products will be updated...')

      counter = 0

      for i in range(len(to_update)):
        id = to_update[i]
        time.sleep(Delay())
        product = GetProduct(session, shop_id, id)

        if not product['prices']: # That happens when product is not available (has been sold during updating)
          print(f"{i + 1}/{len(to_update)} Sold out ({id})")
          continue

        name = Name(products[id])
        ingredients = Ingredients(product)
        cursor.execute(INSERT, (id, ingredients))
        result.append((name, ingredients, Price(products[id])))
        print(f"{i + 1}/{len(to_update)}", 'Updated product with name', f"\"{name}\"")
        counter += 1

        if counter == 10:
          database.commit()
          counter = 0

      if counter > 0:
        database.commit()

    return result
