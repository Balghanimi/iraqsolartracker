import tkinter as tk
from tkinter import ttk, scrolledtext
from datetime import datetime
import pandas as pd
from fuzzywuzzy import fuzz
from scraper_google_cse import search_google as search_google_cse
from scraper_google_cse import search_google
from scraper_opensooq import scrape_opensooq
from database import setup_database
from categorizer import categorize_offer
from telegram_bot import send_to_telegram

class SolarApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Iraq Solar Tracker")
        self.geometry("650x700")

        self.gov_var = tk.StringVar(value="الكل")
        self.google_var = tk.BooleanVar(value=True)
        self.opensooq_var = tk.BooleanVar(value=True)
        self.pdf_var = tk.BooleanVar(value=True)
        self.excel_var = tk.BooleanVar(value=False)
        self.chat_id_var = tk.StringVar()
        self.use_cse_var = tk.BooleanVar(value=True)


        self.create_widgets()

    def create_widgets(self):
        govs = ["الكل", "بغداد", "البصرة", "نينوى", "أربيل", "السليمانية", "الأنبار", "كربلاء"]
        gov_frame = ttk.LabelFrame(self, text="فلتر حسب المحافظة")
        gov_frame.pack(fill="x", padx=10, pady=5)
        for i, gov in enumerate(govs):
            ttk.Radiobutton(gov_frame, text=gov, variable=self.gov_var, value=gov).grid(row=0, column=i)

        source_frame = ttk.LabelFrame(self, text="مصادر البيانات")
        source_frame.pack(fill="x", padx=10, pady=5)
        ttk.Checkbutton(source_frame, text="Google", variable=self.google_var).pack(side="left", padx=10)
        ttk.Checkbutton(source_frame, text="OpenSooq", variable=self.opensooq_var).pack(side="left", padx=10)

        output_frame = ttk.LabelFrame(self, text="خيارات الإخراج")
        output_frame.pack(fill="x", padx=10, pady=5)
        ttk.Checkbutton(output_frame, text="PDF", variable=self.pdf_var).pack(side="left", padx=10)
        ttk.Checkbutton(output_frame, text="Excel", variable=self.excel_var).pack(side="left", padx=10)
        ttk.Checkbutton(source_frame, text="استخدم Google CSE API", variable=self.use_cse_var).pack(side='left', padx=10)


        telegram_frame = ttk.LabelFrame(self, text="إرسال إلى تيليغرام")
        telegram_frame.pack(fill="x", padx=10, pady=5)
        ttk.Entry(telegram_frame, textvariable=self.chat_id_var).pack(side="left", padx=5)
        ttk.Label(telegram_frame, text="Chat ID").pack(side="left", padx=5)

        ttk.Button(self, text="ابحث وعرض النتائج", command=self.run_search).pack(pady=5)
        ttk.Button(self, text="استعلام قاعدة البيانات", command=self.query_db).pack(pady=5)

        fb_frame = ttk.LabelFrame(self, text="📋 لصق منشور من فيسبوك (عرض يدوي)")
        fb_frame.pack(fill="both", padx=10, pady=10)
        self.fb_text = scrolledtext.ScrolledText(fb_frame, height=5, wrap="word")
        self.fb_text.pack(fill="both", padx=5, pady=5)
        ttk.Button(fb_frame, text="📥 أضف العرض إلى النظام", command=self.parse_facebook_offer).pack()

        self.status = ttk.Label(self, text="جاهز", relief="sunken", anchor="w")
        self.status.pack(fill="x", side="bottom")

    def update_status(self, message, success=True):
        self.status.config(text=message)
        self.status.config(foreground="green" if success else "red")
        self.update()

    def parse_facebook_offer(self):
        raw = self.fb_text.get("1.0", "end").strip()
        if not raw:
            self.update_status("الرجاء لصق النص أولاً", success=False)
            return

        lines = raw.split("\n")
        title = lines[0][:40]
        price = next((w for w in raw.split() if w.replace(",", "").isdigit()), "0")
        currency = "IQD"
        governorate = "Unknown"
        category = categorize_offer(title)

        offer = {
            "category": category,
            "title": title,
            "price": float(price.replace(",", "")),
            "currency": currency,
            "governorate": governorate,
            "source": "Facebook (Manual)",
            "link": "manual",
            "date": datetime.now().strftime("%Y-%m-%d")
        }

        import sqlite3
        conn = sqlite3.connect('solar_offers.db')
        conn.execute("INSERT INTO offers (category, title, price, currency, governorate, source, link, date) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                     (offer['category'], offer['title'], offer['price'], offer['currency'], offer['governorate'], offer['source'], offer['link'], offer['date']))
        conn.commit()
        conn.close()

        if self.excel_var.get():
            df = pd.DataFrame([offer])
            excel_name = f"manual_offer_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            df.to_excel(excel_name, index=False)

        self.update_status("✅ تم إضافة عرض فيسبوك يدويًا", success=True)
        self.fb_text.delete("1.0", "end")

    def run_search(self):
        self.update_status("جارٍ البحث...", success=True)
        setup_database()
        offers = []
        gov_filter = self.gov_var.get()

        if self.google_var.get():
    if self.use_cse_var.get():
        google_offers = search_google_cse()
    else:
        google_offers = search_google()

    if selected_gov != "الكل":
        google_offers = [
            o for o in google_offers
            if fuzz.partial_ratio(selected_gov, o.get('governorate', '')) > 80
        ]
    offers.extend(google_offers)

                self.update_status(f"تم جلب {len(google_data)} عرض من Google", success=True)
            except Exception as e:
                self.update_status(f"فشل Google: {e}", success=False)

        if self.opensooq_var.get():
            self.update_status("جارٍ البحث في OpenSooq...", success=True)
            try:
                opensooq_data = scrape_opensooq()
                if gov_filter != "الكل":
                    opensooq_data = [o for o in opensooq_data if fuzz.partial_ratio(gov_filter, o.get('governorate', '')) > 80]
                offers.extend(opensooq_data)
                self.update_status(f"تم جلب {len(opensooq_data)} عرض من OpenSooq", success=True)
            except Exception as e:
                self.update_status(f"فشل OpenSooq: {e}", success=False)

        if not offers:
            self.update_status("لم يتم العثور على عروض", success=False)
            return

        import sqlite3
        conn = sqlite3.connect('solar_offers.db')
        for offer in offers:
            category = categorize_offer(offer['title'], offer.get('snippet', ''))
            conn.execute("INSERT INTO offers (category, title, price, currency, governorate, source, link, date) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                         (category, offer['title'], offer['price'], offer['currency'], offer['governorate'], offer['source'], offer['link'], datetime.now().strftime("%Y-%m-%d")))
        conn.commit()
        conn.close()

        if self.excel_var.get():
            df = pd.DataFrame(offers)
            excel_name = f"solar_offers_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            df.to_excel(excel_name, index=False)
            self.update_status(f"تم تصدير {len(offers)} إلى Excel", success=True)

        if self.chat_id_var.get():
            from telegram_bot import TELEGRAM_TOKEN
            try:
                send_to_telegram(offers, self.chat_id_var.get(), TELEGRAM_TOKEN)
                self.update_status("تم الإرسال إلى Telegram", success=True)
            except Exception as e:
                self.update_status(f"Telegram فشل: {e}", success=False)

        self.update_status(f"اكتمل البحث - تم العثور على {len(offers)} عرض", success=True)

    def query_db(self):
        import sqlite3
        conn = sqlite3.connect('solar_offers.db')
        gov_filter = self.gov_var.get()
        query = "SELECT * FROM offers"
        params = []
        if gov_filter != "الكل":
            query += " WHERE governorate LIKE ?"
            params.append(f"%{gov_filter}%")
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()

        if df.empty:
            self.update_status("لا توجد بيانات في قاعدة البيانات", success=False)
            return

        name = f"db_query_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        df.to_excel(name, index=False)
        self.update_status(f"تم تصدير {len(df)} صفًا إلى {name}", success=True)
