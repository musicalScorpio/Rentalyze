"""

author : Sam Mukherjee

"""
# rentalize_agent_react.py

import requests
import json
from playwright.sync_api import sync_playwright
from typing import List, Dict
from dotenv import load_dotenv
import os


load_dotenv('../env/relatize.env')
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Step 1: Tavily Web Search
def search_with_tavily(address: str) -> List[str]:
    query = f"Recent home sales near {address}, only show Redfin, Zillow, or Realtor.com links."
    response = requests.post(
        "https://api.tavily.com/search",
        headers={"Authorization": f"Bearer {TAVILY_API_KEY}"},
        json={
            "query": query,
            "search_depth": "advanced",
            "include_raw_content": False,
            "include_answer": False
        }
    )
    response.raise_for_status()
    results = response.json().get("results", [])
    urls = [r["url"] for r in results if any(x in r["url"] for x in ["redfin.com", "zillow.com", "realtor.com"])]
    return urls[:5]  # Limit to top 5

# Step 2: Scraper Tool (Playwright)
def scrape_listing(url: str) -> Dict[str, str]:
    from playwright.sync_api import sync_playwright

    sale_price = "Not found"
    sale_date = "Not found"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=60000)

        # Wait for main content to load
        try:
            page.wait_for_selector("body", timeout=10000)

            # Try Redfin layout first
            price_element = page.query_selector("div.home-main-stats span")  # Often contains price
            if price_element:
                sale_price = price_element.inner_text().strip()

            date_elements = page.query_selector_all("div.about-this-home span")  # Check for 'Sold on' text
            for el in date_elements:
                text = el.inner_text()
                if "Sold" in text and "," in text:
                    sale_date = text.replace("Sold:", "").strip()
                    break

        except Exception as e:
            print(f"Error scraping {url}: {e}")

        browser.close()

    return {
        "url": url,
        "sale_price": sale_price,
        "sale_date": sale_date
    }


# Step 3: Agent Controller

def extract_recent_sales(address: str) -> List[Dict[str, str]]:
    urls = search_with_tavily(address)
    sales_data = []
    for url in urls:
        try:
            sale = scrape_listing(url)
            sales_data.append(sale)
        except Exception as e:
            sales_data.append({"url": url, "error": str(e)})
    return sales_data

# Example Usage
if __name__ == "__main__":
    target_address = "123 mainstreet"
    results = extract_recent_sales(target_address)
    print(json.dumps(results, indent=2))