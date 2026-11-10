
import json
import urllib.request

import boto3


S3_BUCKET = "ecommerce-data-engineering-878093321287-us-east-1-an"
API_URL = "https://dummyjson.com/products?limit=0"


def extract_and_upload_products(ingestion_date):

    # 1. Extract products from DummyJSON
    request = urllib.request.Request(
        API_URL,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        data = json.loads(response.read().decode("utf-8"))

    products = data["products"]

    if not products:
        raise ValueError("No products returned by the API")

    # 2. Validate product IDs and required fields
    product_ids = []

    for product in products:
        if product.get("id") is None:
            raise ValueError("A product is missing its ID")

        if not product.get("title") or not product.get("category"):
            raise ValueError(
                f"Product {product['id']} has a missing title or category"
            )

        product_ids.append(product["id"])

    if len(product_ids) != len(set(product_ids)):
        raise ValueError("Duplicate product IDs found in API response")

    # 3. Prepare Redshift-ready records
    normalized_products = []

    for product in products:
        normalized_products.append({
            "product_id": product["id"],
            "title": product.get("title"),
            "category": product.get("category"),
            "price": product.get("price"),
            "stock": product.get("stock"),
            "rating": product.get("rating"),
            "brand": product.get("brand"),
        })

    # 4. Prepare S3 object keys
    raw_s3_key = (
        f"raw/products/"
        f"ingestion_date={ingestion_date}/"
        f"products.json"
    )

    normalized_s3_key = (
        f"raw/products/normalized/"
        f"ingestion_date={ingestion_date}/"
        f"products.jsonl"
    )

    s3 = boto3.client("s3")

    # 5. Upload original API data
    s3.put_object(
        Bucket=S3_BUCKET,
        Key=raw_s3_key,
        Body=json.dumps(
            products,
            ensure_ascii=False
        ).encode("utf-8"),
        ContentType="application/json",
    )

    # 6. Convert normalized records to JSON Lines
    jsonl_content = "\n".join(
        json.dumps(product, ensure_ascii=False)
        for product in normalized_products
    ) + "\n"

    # 7. Upload normalized data
    s3.put_object(
        Bucket=S3_BUCKET,
        Key=normalized_s3_key,
        Body=jsonl_content.encode("utf-8"),
        ContentType="application/json",
    )

    print(f"Successfully extracted {len(products)} products")
    print(f"Raw data uploaded to s3://{S3_BUCKET}/{raw_s3_key}")
    print(f"Normalized data uploaded to s3://{S3_BUCKET}/{normalized_s3_key}")

    # 8. Return S3 locations for downstream tasks
    return {
        "ingestion_date": ingestion_date,
        "raw_s3_key": raw_s3_key,
        "normalized_s3_key": normalized_s3_key,
        "record_count": len(products),
    }
