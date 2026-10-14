import json
from pathlib import Path

input_file = Path("data/raw_products.json")
output_file = Path("data/products.jsonl")

with input_file.open("r", encoding="utf-8") as file:
    products = json.load(file)

with output_file.open("w", encoding="utf-8") as file:
    for product in products:
        file.write(json.dumps(product) + "\n")

print(f"Prepared {len(products)} products.")
print(f"Output: {output_file}")
