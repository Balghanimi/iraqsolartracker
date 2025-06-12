
import tkinter as tk
from tkinter import ttk, scrolledtext
from datetime import datetime
import pandas as pd
from fuzzywuzzy import fuzz

from scraper_google_cse import search_google as search_google_cse
from scraper_google import search_google
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
        govs = ["الكل", "كربلاء", "الأنبار", "البصرة", "السليمانية", "أربيل", "نينوى", "بغداد"]
        gov_frame = ttk.LabelFrame(self, text="فلتر حسب المحافظة")
        gov_frame.pack(fill="x", padx=10, pady=5)
        for i, gov in enumerate(govs):
            ttk.Radiobutton(gov_frame, text=gov, variable=self.gov_var, value=gov).grid(row=0, column=i)

        source_frame = ttk.LabelFrame(self, text="مصادر البيانات")
        source_frame.pack(fill="x", padx=10, pady=5)
        ttk.Checkbutton(source_frame, text="Google", variable=self.google_var).pack(side="left", padx=10)
        ttk.Checkbutton(source_frame, text="OpenSooq", variable=self.opensooq_var).pack(side="left", padx=10)
        ttk.Checkbutton(source_frame, text="استخدم Google CSE API", variable=self.use_cse_var).pack(side="left", padx=10)

        output_frame = ttk.LabelFrame(self, text="خيارات الإخراج")
        output_frame.pack(fill="x", padx=10, pady=5)
        ttk.Checkbutton(output_frame, text="PDF", variable=self.pdf_var).pack(side="left", padx=10)
        ttk.Checkbutton(output_frame, text="Excel", variable=self.excel_var).pack(side="left", padx=10)

        telegram_frame = ttk.LabelFrame(self, text="إرسال إلى تيليغرام")
        telegram_frame.pack(fill="x", padx=10, pady=5)
        ttk.Entry(telegram_frame, textvariable=self.chat_id_var).pack(side="left", padx=5)
        ttk.Label(telegram_frame, text="Chat ID").pack(side="left", padx=5)

        ttk.Button(self, text="ابحث وعرض النتائج", command=self.run_search).pack(pady=10)
        ttk.Button(self, text="استعلام قاعدة البيانات", command=self.query_db).pack(pady=10)

        self.status = ttk.Label(self, text="جاهز", relief='sunken')
        self.status.pack(fill='x', side='bottom')

    def run_search(self):
        self.status.config(text="جارٍ البحث...")
        self.update()

        offers = []
        selected_gov = self.gov_var.get()

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

        if self.opensooq_var.get():
            opensooq_offers = scrape_opensooq()
            if selected_gov != "الكل":
                opensooq_offers = [
                    o for o in opensooq_offers
                    if fuzz.partial_ratio(selected_gov, o.get('governorate', '')) > 80
                ]
            offers.extend(opensooq_offers)

        if not offers:
            self.status.config(text="لم يتم العثور على عروض")
            return

        if self.chat_id_var.get():
            send_to_telegram(offers, self.chat_id_var.get())

        self.status.config(text=f"تم العثور على {len(offers)} عرض")

    def query_db(self):
        self.status.config(text="استعلام غير مفعّل حالياً")
