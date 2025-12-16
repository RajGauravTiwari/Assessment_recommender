import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://www.shl.com"
CATALOG_URL = "https://www.shl.com/products/product-catalog/"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def inspect_pagination():
    response = requests.get(CATALOG_URL, headers=HEADERS, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    pagination_links = set()

    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "product-catalog" in href and ("page" in href or "start" in href or "offset" in href):
            pagination_links.add(urljoin(BASE_URL, href))

    print("Possible pagination URLs found:")
    for link in pagination_links:
        print(link)

if __name__ == "__main__":
    inspect_pagination()
