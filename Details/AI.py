from google import genai
from google.genai import errors

import math
import time
import os

def SendPart(client: genai.Client, content: str, collected: list[tuple]) -> str:
  count = 0
  while True:
    try: # because of often errors on server side, which was annoying
      response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=f'{content}\n{str(collected)}'
      )
      break
    except errors.ServerError:
      print(f'Gemini API error on server with code {response.code_execution_result}, retry')
      count += 1
      if count == 3:
        raise

  return response.text


API_KEY = ''
IDS_INSTRUCTION = 'Ответ отправь в виде списка ID без нумерации (каждый на новой строчке) и только в виде списка ID без нумерации, ID - первый элемент каждого кортежа (число)'
FINAL_INSTRUCTION = 'Ответ отправь в виде списка названий без нумерации и только в виде списка названий без нумерации'
PARTITION = 1400

def Analyse(promt: str, collected: list[tuple]) -> str:
  os.environ['all_proxy'] = 'socks5://127.0.0.1:12334/'
  
  client = genai.Client(
    api_key=API_KEY
  )

  parts_cnt = math.ceil(len(collected) / PARTITION)
  content = f'{promt}\n{IDS_INSTRUCTION}'
  print(f'Part 1/{parts_cnt} sent')
  chosen_ids = [int(x) for x in SendPart(client, content, collected[:PARTITION]).splitlines()]

  for i in range(1, parts_cnt):
    print('Waiting 60 seconds...') # because of token per minute limit
    time.sleep(60)
    print(f'Part {i + 1}/{parts_cnt} sent')
    chosen_ids += [int(x) for x in SendPart(client, content, collected[PARTITION * i: PARTITION * (i + 1)]).splitlines()]

  candidates = [candidate for candidate in collected if candidate[0] in chosen_ids]
  final_content = f'{promt}\n{FINAL_INSTRUCTION}'

  print('Waiting 60 seconds...')
  time.sleep(60)
  print(f'Analysing {parts_cnt} results')
  return SendPart(client, final_content, candidates)
