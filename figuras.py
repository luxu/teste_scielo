import requests
from rich import print

url = "http://localhost:8000/api/v1/xml/?file_xml=scielo_teste_xml_4.xml"

payload = 'usuario=luxu&senha=2'

headers = {'Content-Type': 'application/x-www-form-urlencoded'}

response = requests.post(url, headers=headers, data=payload)

print(response.json())
