import requests
from bs4 import BeautifulSoup

def search_google():
    offers = []
    query = "عروض أنظمة الطاقة الشمسية أسعار مكونات العراق"
    url = f"https://www.google.com/search?q={query}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.find_all('div', class_='tF2Cxc')[:5]
        for result in results:
            title = result.find('h3').text if result.find('h3') else "لا يوجد عنوان"
            snippet = result.find('span', class_='aCOpRe').text if result.find('span', class_='aCOpRe') else ""
            link = result.find('a')['href'] if result.find('a') else "لا يوجد رابط"
            offers.append({
                "title": title,
                "snippet": snippet,
                "price": 0,
                "currency": "Unknown",
                "governorate": "Unknown",
                "source": "Google",
                "link": link
            })
    except Exception as e:
        offers.append({
            "title": "خطأ", "snippet": f"فشل البحث: {e}", "price": 0,
            "currency": "Unknown", "governorate": "Unknown", "source": "Google", "link": "غير متاح"
        })
    return offers
