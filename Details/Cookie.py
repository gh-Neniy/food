from http.cookies import SimpleCookie

def ParseCookie(cookie_str: str) -> dict:
  cookie = SimpleCookie()
  cookie.load(cookie_str)
  
  return {key : value.value for key, value in cookie.items()}
