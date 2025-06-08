from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def scrape_facebook_offers(keyword="طاقة شمسية", max_scroll=3):
    options = Options()
    options.add_argument("--disable-notifications")
    options.add_argument("--headless")  # Remove this if you want to see the browser
    driver = webdriver.Chrome(options=options)

    url = f"https://www.facebook.com/marketplace/iraq/search/?query={keyword}"
    driver.get(url)
    time.sleep(5)  # Allow page to load

    offers = []
    last_height = driver.execute_script("return document.body.scrollHeight")

    for _ in range(max_scroll):
        posts = driver.find_elements(By.XPATH, '//div[contains(@aria-label, "Listing")]')
        for post in posts:
            try:
                title = post.text.split("\n")[0]
                price = post.text.split("\n")[1]
                offers.append({
                    "title": title,
                    "price": price,
                    "currency": "IQD",
                    "governorate": "Unknown",
                    "source": "Facebook",
                    "link": driver.current_url
                })
            except Exception:
                continue

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    driver.quit()
    return offers
