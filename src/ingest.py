
import json
import urllib.request

OUTPUT_FILE = "data/raw_products.json"
URL = "https://dummyjson.com/products?limit=0"


def fetch_products():
    request = urllib.request.Request(
        URL,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    with urllib.request.urlopen(request) as response:
        data = json.loads(response.read())

    products = data["products"]
    expected_count = data["total"]

    if len(products) != expected_count:
        raise ValueError(
            f"Incomplete product fetch: expected {expected_count}, "
            f"but received {len(products)}."
        )

    print(f"Fetched {len(products)} of {expected_count} products.")

    return products


def save_raw_data(products):
    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(products, file, indent=2)


def main():
    products = fetch_products()
    save_raw_data(products)

    print(f"Saved {len(products)} products to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
