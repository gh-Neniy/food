from google import genai
from google.genai import errors

import time

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
  client = genai.Client(
    api_key=api_key
  )

  return Send(client, f'{promt}\n{INSTRUCTION}', collected)
