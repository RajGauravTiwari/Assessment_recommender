import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import json

BASE_URL = "https://www.shl.com"
CATALOG_URL = "https://www.shl.com/products/product-catalog/"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

START_STEP = 12          # SHL offset step
MAX_NO_NEW_PAGES = 5     # stop after 5 consecutive pages with no new links


def extract_links_from_page(start, type_id):
    """
    Fetch a catalog page and extract assessment detail links.
    """
    url = f"{CATALOG_URL}?start={start}&type={type_id}"
    response = requests.get(url, headers=HEADERS, timeout=10)

    if response.status_code != 200:
        return set()

    soup = BeautifulSoup(response.text, "html.parser")
    links = set()

    for a in soup.find_all("a", href=True):
        href = a["href"]

        # Pattern 1: product-catalog detail pages
        if href.startswith("/products/product-catalog/view/"):
            links.add(urljoin(BASE_URL, href))

        # Pattern 2: deep assessment pages
        elif href.startswith("/products/assessments/") and href.count("/") > 4:
            links.add(urljoin(BASE_URL, href))

    return links


def crawl_all_assessments():
    all_links = set()

    for type_id in [1, 2]:
        print(f"\n===== Crawling catalog type={type_id} =====")
        start = 0
        no_new_pages = 0

        while True:
            print(f"Fetching start={start} ... ", end="")

            current_links = extract_links_from_page(start, type_id)
            new_links = current_links - all_links

            if new_links:
                print(f"found {len(new_links)} NEW links")
                all_links.update(new_links)
                no_new_pages = 0
            else:
                print("no new unique links")
                no_new_pages += 1

            # Stop condition
            if no_new_pages >= MAX_NO_NEW_PAGES:
                print("No new links for multiple pages. Stopping this type.")
                break

            start += START_STEP
            time.sleep(0.5)  # be polite to the server

    return all_links


if __name__ == "__main__":
    assessment_links = crawl_all_assessments()

    print("\n==========================================")
    print("Total unique assessment links found:", len(assessment_links))

    # Save results
    output_path = "data/raw/assessment_links.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(sorted(list(assessment_links)), f, indent=2)

    print(f"Saved assessment links to: {output_path}")
