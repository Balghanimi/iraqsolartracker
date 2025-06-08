import sqlite3

def setup_database():
    conn = sqlite3.connect('solar_offers.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS offers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT,
        title TEXT,
        price REAL,
        currency TEXT,
        governorate TEXT,
        source TEXT,
        link TEXT,
        date TEXT)''')
    conn.commit()
    conn.close()
