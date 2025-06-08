def categorize_offer(title, snippet=""):
    keywords = {
        "ألواح شمسية": ["لوح", "ألواح", "شمسي"],
        "محولات": ["محول", "عاكس", "تحويل"],
        "بطاريات": ["بطارية", "بطاريات", "تخزين"],
        "أنظمة كاملة": ["نظام", "أنظمة", "كامل"]
    }
    for category, kws in keywords.items():
        if any(kw in title or kw in snippet for kw in kws):
            return category
    return "أخرى"
