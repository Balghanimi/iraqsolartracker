import requests
from bs4 import BeautifulSoup
import re

def scrape_opensooq():
    url = "https://iq.opensooq.com/ar/find?term=%D8%A7%D9%84%D8%B7%D8%A7%D9%82%D8%A9%20%D8%A7%D9%84%D8%B4%D9%85%D8%B3%D9%8A%D8%A9"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    offers = []
    items = soup.find_all('li', class_='rectLi')[:10]

    for item in items:
        title = item.find('h2').text.strip() if item.find('h2') else "No title"
        price = item.find('span', class_='inline').text.strip() if item.find('span', class_='inline') else "0"
        location = item.find('span', class_='grey').text.strip() if item.find('span', 'grey') else "Unknown"
        link = item.find('a')['href'] if item.find('a') else "#"
        try:
            price_num = float(re.sub(r'[^\d.]', '', price.split()[0])) if price != "0" else 0
            currency = "IQD" if "دينار" in price else "USD"
        except (ValueError, IndexError):
            price_num = 0
            currency = "Unknown"

        offers.append({
            "title": title,
            "snippet": "",
            "price": price_num,
            "currency": currency,
            "governorate": location,
            "source": "OpenSooq",
            "link": f"https://iq.opensooq.com{link}"
        })
    return offers
