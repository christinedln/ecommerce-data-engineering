import json
import urllib.request
OUTPUT_FILE = "data/raw_products.json"

URL = "https://dummyjson.com/products?limit=0"


def fetch_products():
    request =urllib.request.Request(
        URL,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    response =urllib.request.urlopen(request)
    data = json.loads(response.read())
    return data["products"]

def save_raw_data(products):
    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(products, file, indent=2)
    
products = fetch_products()
save_raw_data(products)
print(f"Saved {len(products)} products to {OUTPUT_FILE}")
