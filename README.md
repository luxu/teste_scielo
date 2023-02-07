# Sistema de leitura de arquivos XML

### Postman/Insomnia
Sempre testo os endpoints usando Postam ou Insomnia

Para carregar e salvar na base os XML´s:

via terminal:

``curl --request POST 'http://localhost:8000/api/v1/xml/?file_xml=scielo_teste_xml_3.xml' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'usuario=<usuario>' \
--data-urlencode 'senha=<senha>'``

````import requests
from rich import print
url = "http://localhost:8000/api/v1/xml/?file_xml=scielo_teste_xml_3.xml"
payload='usuario=luxu&senha=2'
headers = { 'Content-Type': 'application/x-www-form-urlencoded'}
response = requests.post(url, headers=headers, data=payload)
print(response.json())
````
Para listar os artigos:

via terminal:

``curl --request GET 'http://localhost:8000/api/v1/artigos/``

````from rich import print
import requests
url = "http://localhost:8000/api/v1/artigos/"
response = requests.get(url)
print(response.json())
````

Foi pensado da seguinte forma o endpoint acima:
- Será passado como argumento o nome do XML de onde será extraído os dados, se exister o mesmo no diretório será feito
a extração, caso contrário, retornará um erro e as opções existentes no diretório atual, ou seja, optando por outro arquivo
o mesmo deverá ser colocado na pasta ``core/files_xml/``





