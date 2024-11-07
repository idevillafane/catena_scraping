import requests
from bs4 import BeautifulSoup
from base64 import b64decode





# Leer URLs desde archivo urls.txt
with open('urls.txt', 'r') as u:
    urls = [url.strip() for url in u.readlines()]

# Iterar sobre las URLs y guardar cada respuesta en un archivo separado
for i, url in enumerate(urls, start=1):
    try:

        api_response = requests.post(
            "https://api.zyte.com/v1/extract",
            auth=("42a0f7111aa9486e84ed7c22bf21129a", ""),
            json={
                "url": url,
                "httpResponseBody": True,
                },
        )
        http_response_body: bytes = b64decode(
            api_response.json()["httpResponseBody"])
        file_name = f'response_{i:03}.html'
        with open(file_name, "wb") as fp:
            fp.write(http_response_body)

        print(f'Se ha guardado la respuesta en {file_name}')
    
    except requests.exceptions.RequestException as e:
        print(f'Error al obtener la URL {url}: {e}')

