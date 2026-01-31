from google import genai

import math
import time
import os

def SendPart(client: genai.Client, part_number: int, content: str, collected: list[tuple]) -> str:
  return client.models.generate_content(
      model="gemini-3-flash-preview",
      contents=f'{content}Часть {part_number}\n{str(collected)}'
  ).text


API_KEY = ''
INSTRUCTION = 'Ответ отправь на последней части в виде списка названий и только в виде списка названий'
PARTITION = 1700

def Analyse(promt: str, collected: list[tuple]) -> str:
  os.environ['all_proxy'] = 'socks5://127.0.0.1:12334/'
  
  client = genai.Client(
    api_key=API_KEY
  )

  parts_cnt = math.ceil(len(collected) / PARTITION)
  content = f'{promt}\nСписок товаров будет отправлен в {parts_cnt} частях.\n{INSTRUCTION}\n'
  print('Part 1 sent')
  response = SendPart(client, 1, content, collected[:PARTITION])

  for i in range(1, parts_cnt):
    print('Waiting 60 seconds...')
    time.sleep(60)
    print(f'Part {i + 1} sent')
    content_continue =  f'{promt}\nУже было отправлено {i} частей из {parts_cnt}.\n{INSTRUCTION}\n'
    response = SendPart(client, i + 1, content_continue, collected[PARTITION * i: PARTITION * (i + 1)])

  return response
