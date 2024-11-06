import requests
from bs4 import BeautifulSoup

# Leer los encabezados desde el archivo 'headers.txt' y convertirlos en un diccionario
headers = {}
with open('headers.txt', 'r') as file:
    for line in file.readlines():
        if ':' in line:
            key, value = line.split(':', 1)
            headers[key.strip()] = value.strip()

with open('urls.txt', 'r') as file:
    urls = file.readlines()

for url in urls: 
   
    url = url.strip()
    
    try:
    
        response = requests.get(url, headers=headers)

        if response.status_code == 200:

            soup = BeautifulSoup(response.text, 'html.parser')

            content = response.text

            filename = 'wine_searcher_page.txt'

            with open(filename, 'w', encoding='utf-8') as file:
                file.write(content)
        
            merchant_name_tag = soup.find('a', class_='offer-card__merchant-name')

            merchant_name = merchant_name_tag.get_text(strip=True)

            print(merchant_name)

        print(f"Respuesta de {url}: {response.status_code}") 

    except requests.exceptions.RequestException as e: 
    
        print(f"Error al hacer GET a {url}: {e}")


