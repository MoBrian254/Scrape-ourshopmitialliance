import requests
from bs4 import BeautifulSoup
import sqlite3

# URL to scrape
url = "https://miti.co.ke/our-shop/"

# HEADER info
headers = {
  'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0.2; SM-T535) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.74 Safari/537.36'
}

# Make a GET request to the URL
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Connect to SQLite3 database
    conn = sqlite3.connect('items.db')
    cursor = conn.cursor()

    # Create a table to store scraped data if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image TEXT,
            name TEXT,
            price TEXT
        )
    ''')

    # Find and extract relevant information
    for product in soup.find_all('div', class_='product-item'):
        image = product.find('img')['src']
        name = product.find('h2', class_='woocommerce-loop-product__title').text.strip()
        price = product.find('span', class_='woocommerce-Price-amount').text.strip()

        # Insert data into the database
        cursor.execute('''
            INSERT INTO items (image, name, price) VALUES (?, ?, ?)
        ''', (image, name, price))
    
    # Commit changes and close the database connection
    conn.commit()
    conn.close()

    print("Scraping and database insertion completed.")
else:
    print("Failed to retrieve the page. Status code:", response.status_code)
