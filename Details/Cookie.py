from http.cookies import SimpleCookie

def ParseCookie(cookie_str: str) -> dict:
  cookie = SimpleCookie()
  cookie.load(cookie_str)
  return {key : value.value for key, value in cookie.items()}


def SaveCookie(cookie_path: str, cookie_str: str) -> None:
  with open(cookie_path, 'w') as cookie:
    cookie.write(cookie_str)


def ReadCookie(cookie_path: str) -> dict:
  with open(cookie_path, 'r') as cookie:
    return ParseCookie(cookie.read())
