import requests
from bs4 import BeautifulSoup

# Credenciales para Web Unblocker
USERNAME, PASSWORD = 'merovingiandata_ZjXlY', 'AguanteColombia22++'

# Proxy
proxies = {
  'http': f'http://{USERNAME}:{PASSWORD}@unblock.oxylabs.io:60000',
  'https': f'https://{USERNAME}:{PASSWORD}@unblock.oxylabs.io:60000',
}

SCRAPERAPI_KEY = '505e4a02aa851987b48f861bae7a59a3'

# Leer headers desde archivo headers.txt en el formato especificado
headers = {}
with open('headers.txt', 'r') as h:
    key = None
    for line in h:
        line = line.strip()
        if not line:  # Saltar líneas en blanco
            continue
        if ':' in line:  # Línea de encabezado (clave: valor)
            key, value = line.split(':', 1)
            headers[key.strip()] = value.strip()
        elif key:  # Línea sin ":". Se añade al valor del encabezado previo
            headers[key] += f' {line.strip()}'


# Leer URLs desde archivo urls.txt
with open('urls.txt', 'r') as u:
    urls = [url.strip() for url in u.readlines()]

# Iterar sobre las URLs y guardar cada respuesta en un archivo separado
for i, url in enumerate(urls, start=1):
    response = requests.get(
        url=f"http://api.scraperapi.com/?api_key={SCRAPERAPI_KEY}&url={url}",
        headers=headers,
        # proxies=proxies,
        verify=False  # Ignorar el certificado SSL
    )
    
    # Guardar el HTML de cada respuesta en un archivo único
    file_name = f'response_{i:03}.html'
    with open(file_name, 'w') as f:
        f.write(response.text)
    
    print(f'Se ha guardado la respuesta en {file_name}')

