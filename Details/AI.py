from google import genai

import os

API_KEY = ''

def Analyse(collected: list[tuple]) -> str:
  os.environ['HTTPS_PROXY'] = 'socks5://127.0.0.1:12334/'
  os.environ['GEMINI_API_KEY'] = API_KEY
  client = genai.Client()

  return client.models.generate_content(
      model="gemini-3-flash-preview",
      contents='Choose for me top 10 products without sugar and send as python list with these names.\nOnly python list in output.\n' + str(collected[:200])
  )
