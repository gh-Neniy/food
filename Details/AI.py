from google import genai
from google.genai import errors, types

import time
import os


def ProxyFromEnv() -> str | None:
  for name in ('HTTPS_PROXY', 'https_proxy', 'ALL_PROXY', 'all_proxy'):
    url = os.environ.get(name)
    if url:
      if url.startswith('socks://'):
        url = 'socks5://' + url[len('socks://'):]
      return url
      
  return None

def Send(client: genai.Client, content: str, collected: list[tuple]) -> str:
  count = 0

  while True:
    try: # because of often errors on server side, which was annoying
      last_send_time = time.time()

      response = client.models.generate_content(
        model="gemini-3.1-pro-preview",
        contents=f'{content}\n{str(collected)}'
      )

      break
    except errors.ServerError as error:
      print(f'Gemini API error on server {error}, retry')
      count += 1

      time_to_wait = 60.0 - (time.time() - last_send_time)

      if time_to_wait > 0:
        print(f"Waiting {round(time_to_wait, 2)} seconds...")
        time.sleep(time_to_wait)

      if count == 3:
        raise

  return response.text


INSTRUCTION = 'Ответ отправь в виде списка названий без нумерации и только в виде списка названий без нумерации'

def Analyse(api_key: str, promt: str, collected: list[tuple]) -> str:
  proxy = ProxyFromEnv()
  http_options = None

  if proxy:
    http_options = types.HttpOptions(
      client_args={'proxy': proxy, 'trust_env': False},
      async_client_args={'proxy': proxy, 'trust_env': False},
    )

  client = genai.Client(
    api_key=api_key,
    http_options=http_options,
  )

  return Send(client, f'{promt}\n{INSTRUCTION}', collected)
