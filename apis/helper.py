from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_zumper_rentals(zipcode, max_results=10):
    options = Options()
    options.headless = False  # Set to True to run headless
    driver = webdriver.Chrome(options=options)

    url = f"https://www.zumper.com/apartments-for-rent/ocala-fl/{zipcode}"
    driver.get(url)



    listings = []
    cards = driver.find_elements(By.ID, 'results')[:max_results]  # Update selector as needed

    for card in cards:
        try:
            address = card.find_element(By.CSS_SELECTOR, 'ListingCardContentSection_detailLinkText__kjqHB').text  # Update selector
            price = card.find_element(By.CSS_SELECTOR, 'ListingCardContentSection_longTermPrice__TkxdS ListingCardContentSection_longTermPriceLargeCard__jcX43').text  # Update selector
            specs = card.find_element(By.CSS_SELECTOR, 'ListingCardContentSection_bedsRangeText__BF7nu ListingCardContentSection_bathRangeTextLongTerm__vpJpD ListingCardContentSection_bedsRangeTextLargeCard__98N9Z').text  # Update selector
            # Parse specs into beds, baths, and type as needed
        except Exception as e:
            address = price = specs = "N/A"

        listings.append({
            "address": address,
            "price": price,
            "specs": specs,
            # Add more fields as needed
        })

    driver.quit()
    return listings

# Example usage
results = get_zumper_rentals("34473", max_results=5)
for r in results:
    print(r)
