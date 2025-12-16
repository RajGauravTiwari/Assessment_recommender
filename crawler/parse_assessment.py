import requests
from bs4 import BeautifulSoup
import json
import time
import re
from pathlib import Path

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

NOISE_PATTERNS = [
    r"we recommend upgrading.*",
    r"latest browser options.*",
    r"cookie.*",
    r"privacy.*",
]

RAW_LINKS_PATH = "data/raw/assessment_links.json"
OUTPUT_PATH = "data/processed/assessments.json"


def clean_text(text: str) -> str:
    text = text.lower()
    for pattern in NOISE_PATTERNS:
        text = re.sub(pattern, "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_description(soup: BeautifulSoup) -> str:
    collected = []

    for heading in soup.find_all(["h2", "h3"]):
        title = heading.get_text(strip=True).lower()
        if any(k in title for k in ["overview", "description", "what", "measure"]):
            for sib in heading.find_next_siblings():
                if sib.name in ["h2", "h3"]:
                    break
                collected.append(sib.get_text(" ", strip=True))

    if collected:
        return clean_text(" ".join(collected))

    main = soup.find("main")
    if main:
        return clean_text(main.get_text(" ", strip=True))

    return ""


def parse_assessment_page(url: str) -> dict | None:
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        name_tag = soup.find("h1")
        name = name_tag.get_text(strip=True) if name_tag else None

        description = extract_description(soup)

        page_text = soup.get_text(" ", strip=True).lower()
        is_individual = not (
            "pre-packaged" in page_text or
            "job solution" in page_text
        )

        if not name or not is_individual:
            return None

        return {
            "assessment_name": name,
            "description": description,
            "url": url
        }

    except Exception as e:
        print("Error parsing:", url, e)
        return None


def main():
    Path("data/processed").mkdir(parents=True, exist_ok=True)

    with open(RAW_LINKS_PATH, "r", encoding="utf-8") as f:
        urls = json.load(f)

    results = []
    total = len(urls)

    print(f"Parsing {total} assessment pages...\n")

    for idx, url in enumerate(urls, start=1):
        print(f"[{idx}/{total}] Parsing: {url}")
        data = parse_assessment_page(url)

        if data:
            results.append(data)

        time.sleep(0.5)  # polite crawling

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print("\n===================================")
    print("Parsing complete.")
    print("Total Individual Test Solutions:", len(results))
    print("Saved to:", OUTPUT_PATH)


if __name__ == "__main__":
    main()
