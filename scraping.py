import requests
from bs4 import BeautifulSoup
import csv
import time

BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"
HEADER = {
    "User-Agent": "Mozilla/5.0"
}

def get_book_data(soup):
    books = []
    for book in soup.select(".product_pod"):
        title = book.h3.a["title"]
        price = book.select_one(".price_color").text
        availability = book.select_one(".instock.availability").text.strip()
        books.append([title, price, availability])
    return books

def main():
    all_books = []
    for page in range(1, 51):
        print(f"Scraping website page {page}")
        url = BASE_URL.format(page)
        response = requests.get(url, headers=HEADER)

        if response.status_code != 200:
            print(f"Failed to fetch the page {page}")
            break

        soup = BeautifulSoup(response.text, "lxml")
        books = get_book_data(soup)
        all_books.extend(books)

        time.sleep(1)

    # Write to CSV after all pages are scraped
    with open("books.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Title", "Price", "Availability"])
        writer.writerows(all_books)

    print("Scraping is done! Data saved to books.csv")

if __name__ == "__main__":
    main()
