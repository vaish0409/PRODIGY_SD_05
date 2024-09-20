import requests
from bs4 import BeautifulSoup
import csv

def scrape_products(url):
    # Send a request to the website
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    # Extract product information
    products = []
    for product in soup.find_all("article", class_="product_pod"):  # Correct class for product container
        name = product.h3.a["title"]  # Extract the product title
        price = product.find("p", class_="price_color").text.strip()  # Extract the price
        rating = product.p["class"][1]  # Extract the rating, which is stored in a class like "star-rating Three"
        
        products.append([name, price, rating])

    return products

def save_to_csv(products, filename="products.csv"):
    # Save the scraped data to a CSV file
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Product Name", "Price", "Rating"])
        writer.writerows(products)

if __name__ == "__main__":
    url = "http://books.toscrape.com/catalogue/page-2.html"  # URL to scrape
    # url = "https://coinmarketcap.com/all/views/all/"
    products = scrape_products(url)
    save_to_csv(products)
    print(f"Scraped {len(products)} products and saved to 'products.csv'")
