# IraqSolarTracker - Solar Offers Tracker for Iraq

A Python application to track solar system offers in Iraq, also known as "شمس العراق" (Shams Al-Iraq). It scrapes offers from Google, OpenSooq, and supports manual Facebook offer input, with a Tkinter GUI, SQLite database, and Excel/Telegram outputs.

## Features
- **Scraping**: Automated scraping from Google and OpenSooq.
- **Manual Input**: Paste Facebook posts for parsing.
- **Categorization**: Organizes offers into categories (e.g., ألواح شمسية, محولات).
- **Outputs**: Generates Excel files and (planned) PDF reports.
- **Database**: Stores offers in SQLite for historical tracking.
- **GUI**: Arabic interface with governorate filters and output options.
- **Telegram**: Sends results to a Telegram chat (optional).

## Installation
1. Install Python 3.8+.
2. Clone the repository:
   ```bash
   git clone https://github.com/Balghanimi/iraqsolartracker.git
   cd iraqsolartracker
