from curl_cffi import requests
from Details.Cookie import *
from Details.Products import GetCategories, GetProducts
from Details.Database import CollectData
from Details.AI import Analyse

import sys
import os

def main():
  cookie_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Details', 'Cookie')
  if len(sys.argv) > 2:
    print("Invalid argument count.")
    sys.exit(-1)

  if len(sys.argv) == 2:
    if sys.argv[1] != '--update-cookie':
      print("Unknown flag.")
      sys.exit(-1)

    print('Enter the cookie:')
    cookie_str = input()
    SaveCookie(cookie_path, cookie_str)
    cookies = ParseCookie(cookie_str)
  else:
    cookies = ReadCookie(cookie_path)

  with requests.Session(cookies=cookies, impersonate='chrome136') as session:
    products_id = GetProducts(session, GetCategories(session))
    print('Received', len(products_id), 'products')
    collected = CollectData(session, products_id)
    print(len(collected))
    print('Promt send')
    print(Analyse(collected))
    
  
if __name__ == '__main__':
  main()
