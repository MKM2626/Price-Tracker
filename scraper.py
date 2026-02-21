import sqlite3
import time
import subprocess
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

# CONFIGURATION 
load_dotenv()
HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}
CHECK_INTERVAL = 3600  # Check every hour (3600 seconds)
DB_NAME = "tracker.db" # Local SQL database

def notify_mac(title, text):
    """Sends a native macOS system notification."""
    script = f'display notification "{text}" with title "{title}"'
    subprocess.run(['osascript', '-e', script])

def init_db():
    """Creates the database table if it doesn't exist."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS products 
                 (id INTEGER PRIMARY KEY, name TEXT, url TEXT, target_price REAL)''')
    
    conn.commit()
    conn.close()

def get_price(url):
    """Scrapes price from URL. Returns None if fails."""
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.content, "html.parser")
        
        # NOTE: You must customize this selector based on the website!
        # Example: looking for <span class="a-offscreen">
        price_element = soup.select_one(".price-tag, .a-offscreen, #priceblock_ourprice")
        
        if price_element:
            price_str = price_element.get_text().replace("$", "").replace(",", "").strip()
            return float(price_str)
        return None
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

def main_loop():
    """The background engine."""
    init_db()
    notify_mac("Tracker Active", "The Price Tracker is now running in the background.")
    
    while True:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT name, url, target_price FROM products")
        items = c.fetchall()
        
        for name, url, target in items:
            current_price = get_price(url)
            
            if current_price is not None:
                print(f"Checking {name}: ${current_price}")
                if current_price <= target:
                    notify_mac("💰 Price Drop!", f"{name} is now ${current_price}!")
            else:
                print(f"Skipped {name} due to scraping error.")
        
        conn.close()
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main_loop()