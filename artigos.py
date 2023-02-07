from rich import print
import requests

url = "http://localhost:8000/api/v1/artigos/"

response = requests.get(url)

print(response.json())
