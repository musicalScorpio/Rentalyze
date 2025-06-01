"""

author : Sam Mukherjee

"""
import requests
import os
from dotenv import load_dotenv
import pydeck as pdk
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
"""
# Load environment variables from .env file
#load_dotenv('../env/relatize.env')
#RENTCAST_API_KEY = os.getenv("RENTCAST_API_KEY")
def get_zip_rent(zip_code, bedrooms):
    api_key = {RENTCAST_API_KEY}  # Sign up at rentcast.io
    endpoint = f"https://api.rentcast.io/v1/rents?zip={zip_code}&bedrooms={bedrooms}"
    headers = {"X-Api-Key": api_key}

    response = requests.get(endpoint, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.text}

"""


def get_fmr_data(zip_code="34473"):
    url = f"https://www.rentdata.org/lookup?zip={zip_code}"

    options = Options()
    options.headless = False  # Set to True to run in background
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/123.0.0.0 Safari/537.36")
    driver = webdriver.Chrome(options=options)

    driver.get(url)

    try:
        # Wait for the rent table to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//table"))
        )
        table = driver.find_element(By.XPATH, "//table")
        rows = table.find_elements(By.TAG_NAME, "tr")

        fmr_data = {}
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "th")
            if len(cols) == 2:
                bedroom_type = cols[1].text.strip()
                rent = row.find_elements(By.TAG_NAME, "td")[0].text.strip()
                fmr_data[bedroom_type] = rent

        return fmr_data

    except Exception as e:
        print(f"Error: {e}")
        return {}

    finally:
        driver.quit()