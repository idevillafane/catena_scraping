import requests
from bs4 import BeautifulSoup

# Use your Web Unblocker credentials here.
USERNAME, PASSWORD = 'merovingiandata_ZjXlY', 'AguanteColombia22++'

# Define proxy dict.
proxies = {
  'http': f'http://{USERNAME}:{PASSWORD}@unblock.oxylabs.io:60000',
  'https': f'https://{USERNAME}:{PASSWORD}@unblock.oxylabs.io:60000',
}

# URLs to scrape
url = "https://www.wine-searcher.com/find/Angelica+Zapata+Cabernet+Franc/1/us-ar?Xcurrencycode=USD&Xsort_order=p&Xsavecurrency=Y"


with open('headers.txt', 'r') as h:
    headers = h.readlines()

response = requests.request(
    'GET',
    url,
    verify=False,  # Ignore the SSL certificate
    proxies=proxies,
)

# Print result page to stdout
print(response.text)

# Save returned HTML to result.html file
with open('result.html', 'w') as f:
    f.write(response.text)

'''
# Define headers to mimic a browser request
headers = {
    "authority": "www.wine-searcher.com",
    "method": "GET",
    "path": "/merchant/26586-total-wine-more-brea?wine_id_F=413780600",
    "scheme": "https",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.9,es;q=0.8,es-AR;q=0.7,es-ES;q=0.6",
    "cookie": """cookie_enabled=true; ID=8J32C5N9KZ5008K; ...""",  # truncated for brevity
    "priority": "u=0, i",
    "referer": "https://www.wine-searcher.com/find/catena+zapata+angelica+alta+cab+franc+mendoza+argentina/1/usa-ca?Xsort_order=p",
    "sec-ch-ua": "\"Chromium\";v=\"130\", \"Microsoft Edge\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0"
}
'''

'''
for url in urls:
    try:
        # Use Oxylabs proxy with requests
        response = requests.get(
            url,
            headers=headers,
            proxies=oxylabs_proxy.get_proxies(),
            timeout=10
        )

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Example of extracting merchant name
            merchant_name_tag = soup.find('a', class_='offer-card__merchant-name')
            if merchant_name_tag:
                merchant_name = merchant_name_tag.get_text(strip=True)
                print(f"Merchant Name: {merchant_name}")
            else:
                print("Merchant name not found on this page.")
        else:
            print(f"Failed to retrieve {url}. Status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Error while making GET request to {url}: {e}")
'''
