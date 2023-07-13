import requests

url = "https://api.countrystatecity.in/v1/states"

headers = {
  'X-CSCAPI-KEY': 'API_KEY'
}

response = requests.request("GET", url, headers=headers)

print(response.text)