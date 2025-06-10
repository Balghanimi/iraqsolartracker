from gui import SolarApp  
from scraper_google_cse import search_google

offers = search_google("منظومة طاقة شمسية العراق")
for offer in offers:
    print(offer["title"], offer["link"])

if __name__ == "__main__":
    app = SolarApp()
    app.mainloop()
