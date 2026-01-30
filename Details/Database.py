from curl_cffi import requests
from Details.Products import GetProduct
from Details.SQLCode import SELECT_ID_UPDATE, SELECT_ESSENTIALS, INSERT
from Details.Delay import Delay

import mysql.connector as sql
import time
import re

WEEK_SEC = 604800

def Name(product: dict) -> str:
  words = product['name'].split() # leaves only clear words list, without escape sequences
  result_words = words[:3]
  if len(words) <= 3:
    return ' '.join(result_words)
  
  if result_words[-1] in ['с', 'в', 'из', 'и', 'от', 'со'] or result_words[-1].isdigit():
    del result_words[-1]

  result_words.append(words[-1])
  return ' '.join(result_words)


def Composition(product: dict) -> str:
  composition = product['ingredients']
  if composition == None:
    return ''
  
  sentences = re.sub(r'(\d),\s+(\d)', r'\1,\2', composition).split('. ')
  filtered = [sentence for sentence in sentences if 'предприят' not in sentence.lower()]
  return '. '.join(filtered)


def Price(product: dict) -> str:
  if len(product['prices']) == 1 or product['prices'][0]['placement_type'] == 'promotional_primary':
    return product['prices'][0]['value']
  return product['prices'][1]['value']


def UpdateData(session: requests.Session, products_id: list[str]) -> list[tuple]:
  with sql.connect(host='localhost', user='food', password='yandextop') as database:
    with database.cursor() as cursor:
      cursor.execute(SELECT_ID_UPDATE)
      id_update = {str(row[0]) : row[1] for row in cursor.fetchall()}

      to_update = []
      for id in products_id:
        if id not in id_update or id_update[id].timestamp() + WEEK_SEC < time.time():
          to_update.append(id)

      if len(to_update) > 0:
        print(len(to_update), 'products will be updated...')

        counter = 0
        for i in range(len(to_update)):
          time.sleep(Delay())
          product = GetProduct(session, to_update[i])
          if len(product['prices']) == 0: # That happens when product is not available (has been sold during updating)
            print(f"{i + 1}/{len(to_update)} Sold out")
            continue

          product_name = Name(product)
          cursor.execute(INSERT, (to_update[i], product_name, Composition(product), Price(product)))
          print(f"{i + 1}/{len(to_update)}", 'Updated product with name', f"\"{product_name}\"")
          counter += 1
          if counter == 10:
            database.commit()
            counter = 0

        if counter > 0:
          database.commit()

      cursor.execute(SELECT_ESSENTIALS)
      return [(row[1], row[2], float(row[3])) for row in cursor.fetchall() if str(row[0]) in products_id]
