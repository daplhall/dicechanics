import requests
import time 
import numpy as np

def anydice(query):
  req = requests.post('https://anydice.com/calculator_limited.php', 
    headers={
      'accept': 'application/json, text/javascript, */*', 
      'accept-language': 'da-DK,da;q=0.9,en-US;q=0.8,en;q=0.7,nb;q=0.6,es;q=0.5', 
      'content-type': 'application/x-www-form-urlencoded', 
      'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"', 
      'sec-ch-ua-mobile': '?0', 
      'sec-ch-ua-platform': '"Windows"', 
      'sec-fetch-dest': 'empty', 
      'sec-fetch-mode': 'cors', 
      'sec-fetch-site': 'same-origin', 
      'x-requested-with': 'XMLHttpRequest', 
      'referer': 'https://anydice.com/', 
      'referrer-policy': 
      'strict-origin-when-cross-origin'
     }, 
     data = "program=" + requests.utils.quote(query)
  )
  time.sleep(0.400)
  req_data = req.json()
  res = {}
  if 'error' in req_data:
    raise Exception("Anydice - " + req_data['error']['type'] + ": " + req_data['error']['message'])
  else :
    data = req_data["distributions"]['data']
    labels = req_data["distributions"]['labels']
    for values, key in zip(data, labels):
      faces = np.array([x[0] for x in values])
      prop  = np.array([x[1] for x in values])/100
      res[key] = {"values" : faces, "prop" : prop}
  return res


if __name__ == '__main__':
  data = anydice(
    """
      output 1d6 named "1d6"
      output 2d6 named "2d6"
    """
  )
  print("hello")