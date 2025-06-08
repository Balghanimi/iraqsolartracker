
import re

def parse_facebook_text_arabic(text):
    # Normalize Arabic numerals and commas
    text = text.replace(",", "").replace("،", "")

    # Extract price
    price_match = re.search(r"(\d{4,})\s*(د\.ع|دينار|IQD)?", text)
    price = int(price_match.group(1)) if price_match else 0
    currency = "IQD" if price_match else "Unknown"

    # Extract governorate (improved list)
    governorates = [
        "بغداد", "البصرة", "نينوى", "أربيل", "السليمانية", "الأنبار", "كربلاء",
        "النجف", "ذي قار", "ديالى", "كركوك", "صلاح الدين", "واسط", "المثنى",
        "ميسان", "الديوانية", "بابل"
    ]
    found_gov = next((g for g in governorates if g in text), "غير معروف")

    # Determine category based on keywords
    categories = {
        "ألواح شمسية": ["لوح", "ألواح", "شمسي", "خلايا"],
        "محولات": ["محول", "عاكس", "تحويل", "انفرتر", "hybrid"],
        "بطاريات": ["بطارية", "بطاريات", "تخزين"],
        "أنظمة كاملة": ["نظام", "منظومة", "كامل", "كاملة"]
    }
    detected_category = "أخرى"
    for cat, kws in categories.items():
        if any(kw in text for kw in kws):
            detected_category = cat
            break

    # Short title extraction
    title = text.strip().split("\n")[0][:60]

    return {
        "title": title,
        "price": price,
        "currency": currency,
        "governorate": found_gov,
        "category": detected_category
    }
