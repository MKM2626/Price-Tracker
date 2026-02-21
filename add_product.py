import sqlite3

def add_item(name, url, target_price):
    conn = sqlite3.connect('tracker.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS products 
                 (id INTEGER PRIMARY KEY, name TEXT, url TEXT, target_price REAL)''')
    
    c.execute("INSERT INTO products (name, url, target_price) VALUES (?, ?, ?)", 
              (name, url, target_price))
    
    conn.commit()
    conn.close()
    print(f"✅ Added {name} to your list! Target: ${target_price}")

if __name__ == "__main__":
    # Change these three values to whatever you want to track!
    name = input("Enter product name: ")
    url = input("Enter product URL: ")
    price = float(input("Enter target price: "))
    add_item(name, url, price)