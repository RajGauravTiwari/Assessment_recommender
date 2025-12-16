import json
from urllib.parse import urlparse

CLEAN_DATA_PATH = "data/processed/assessments_clean.json"


def normalize_url(url: str) -> str:
    """
    Normalize URLs so that minor differences (trailing slash, http/https)
    do not cause mismatches.
    """
    parsed = urlparse(url.strip())
    return parsed.scheme + "://" + parsed.netloc + parsed.path.rstrip("/")


def load_clean_urls():
    with open(CLEAN_DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    return {normalize_url(item["url"]) for item in data}


def check_urls(urls_to_check):
    clean_urls = load_clean_urls()

    present = []
    missing = []

    for url in urls_to_check:
        if normalize_url(url) in clean_urls:
            present.append(url)
        else:
            missing.append(url)

    print("\n========== CHECK RESULTS ==========")
    print(f"Total URLs checked: {len(urls_to_check)}")
    print(f"Found in clean dataset: {len(present)}")
    print(f"Missing from clean dataset: {len(missing)}")

    print("\n--- ✅ PRESENT ---")
    for u in present:
        print(u)

    print("\n--- ❌ MISSING ---")
    for u in missing:
        print(u)


if __name__ == "__main__":

    URLS_TO_CHECK = [
        "https://www.shl.com/solutions/products/product-catalog/view/automata-fix-new/",
        "https://www.shl.com/solutions/products/product-catalog/view/core-java-entry-level-new/",
        "https://www.shl.com/solutions/products/product-catalog/view/java-8-new/",
        "https://www.shl.com/solutions/products/product-catalog/view/core-java-advanced-level-new/",
        "https://www.shl.com/products/product-catalog/view/interpersonal-communications/",
        "https://www.shl.com/solutions/products/product-catalog/view/entry-level-sales-7-1/",
        "https://www.shl.com/solutions/products/product-catalog/view/entry-level-sales-sift-out-7-1/",
        "https://www.shl.com/solutions/products/product-catalog/view/entry-level-sales-solution/",
        "https://www.shl.com/solutions/products/product-catalog/view/sales-representative-solution/",
        "https://www.shl.com/products/product-catalog/view/business-communication-adaptive/",
        "https://www.shl.com/solutions/products/product-catalog/view/technical-sales-associate-solution/",
        "https://www.shl.com/solutions/products/product-catalog/view/svar-spoken-english-indian-accent-new/",
        "https://www.shl.com/solutions/products/product-catalog/view/english-comprehension-new/",
        "https://www.shl.com/products/product-catalog/view/enterprise-leadership-report/",
        "https://www.shl.com/products/product-catalog/view/occupational-personality-questionnaire-opq32r/",
        "https://www.shl.com/solutions/products/product-catalog/view/opq-leadership-report/",
        "https://www.shl.com/solutions/products/product-catalog/view/opq-team-types-and-leadership-styles-report",
        "https://www.shl.com/products/product-catalog/view/enterprise-leadership-report-2-0/",
        "https://www.shl.com/solutions/products/product-catalog/view/global-skills-assessment/",
        "https://www.shl.com/solutions/products/product-catalog/view/verify-verbal-ability-next-generation/",
        "https://www.shl.com/solutions/products/product-catalog/view/shl-verify-interactive-inductive-reasoning/",
        "https://www.shl.com/solutions/products/product-catalog/view/marketing-new/",
        "https://www.shl.com/solutions/products/product-catalog/view/drupal-new/",
        "https://www.shl.com/solutions/products/product-catalog/view/written-english-v1/",
        "https://www.shl.com/solutions/products/product-catalog/view/search-engine-optimization-new/",
        "https://www.shl.com/solutions/products/product-catalog/view/automata-selenium/",
        "https://www.shl.com/products/product-catalog/view/professional-7-1-solution/",
        "https://www.shl.com/solutions/products/product-catalog/view/javascript-new/",
        "https://www.shl.com/solutions/products/product-catalog/view/htmlcss-new/",
        "https://www.shl.com/solutions/products/product-catalog/view/css3-new/",
        "https://www.shl.com/solutions/products/product-catalog/view/selenium-new/",
        "https://www.shl.com/solutions/products/product-catalog/view/sql-server-new/",
        "https://www.shl.com/solutions/products/product-catalog/view/automata-sql-new/",
        "https://www.shl.com/solutions/products/product-catalog/view/manual-testing-new/",
        "https://www.shl.com/solutions/products/product-catalog/view/administrative-professional-short-form/",
        "https://www.shl.com/solutions/products/product-catalog/view/verify-numerical-ability/",
        "https://www.shl.com/solutions/products/product-catalog/view/financial-professional-short-form/",
        "https://www.shl.com/solutions/products/product-catalog/view/bank-administrative-assistant-short-form/",
        "https://www.shl.com/solutions/products/product-catalog/view/general-entry-level-data-entry-7-0-solution/",
        "https://www.shl.com/solutions/products/product-catalog/view/basic-computer-literacy-windows-10-new/",
        "https://www.shl.com/solutions/products/product-catalog/view/manager-8-0-jfa-4310/",
        "https://www.shl.com/solutions/products/product-catalog/view/microsoft-excel-365-essentials-new/",
        "https://www.shl.com/solutions/products/product-catalog/view/digital-advertising-new/",
        "https://www.shl.com/solutions/products/product-catalog/view/writex-email-writing-sales-new/",
        "https://www.shl.com/solutions/products/product-catalog/view/shl-verify-interactive-numerical-calculation/",
        "https://www.shl.com/solutions/products/product-catalog/view/sql-server-analysis-services-%28ssas%29-%28new%29/",
        "https://www.shl.com/solutions/products/product-catalog/view/python-new/",
        "https://www.shl.com/solutions/products/product-catalog/view/tableau-new/",
        "https://www.shl.com/solutions/products/product-catalog/view/microsoft-excel-365-new/",
        "https://www.shl.com/solutions/products/product-catalog/view/professional-7-0-solution-3958/",
        "https://www.shl.com/solutions/products/product-catalog/view/data-warehousing-concepts/"
    ]

    check_urls(URLS_TO_CHECK)
