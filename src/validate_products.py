import json
from pathlib import Path

INPUT_FILE = Path("data/raw_products.json")


def validate_products(products):
    errors = []
    seen_ids = set()

    for index, product in enumerate(products):
        row_number = index + 1

        # Check whether the product ID exists.
        product_id = product.get("id")

        if product_id is None:
            errors.append(
                f"Row {row_number}: missing product ID"
            )
        elif product_id in seen_ids:
            errors.append(
                f"Row {row_number}: duplicate product ID "
                f"{product_id}"
            )
        else:
            seen_ids.add(product_id)

        # Check whether the title is present.
        title = product.get("title")

        if not isinstance(title, str) or not title.strip():
            errors.append(
                f"Row {row_number}: missing or empty title"
            )

        # Check whether the category is present.
        category = product.get("category")

        if not isinstance(category, str) or not category.strip():
            errors.append(
                f"Row {row_number}: missing or empty category"
            )

        # Check whether the price is valid.
        price = product.get("price")

        if (
            isinstance(price, bool)
            or not isinstance(price, (int, float))
            or price < 0
        ):
            errors.append(
                f"Row {row_number}: invalid price {price!r}"
            )

        #Check stock
        stock = product.get("stock")

        if (
            isinstance(stock, bool)
            or not isinstance(stock, int)
            or stock < 0
        ):
            errors.append(
            f"Row {row_number}: invalid stock {stock!r}"
            )

        # Check rating.
        rating = product.get("rating")

        if (
            isinstance(rating, bool)
            or not isinstance(rating, (int, float))
            or not 0 <= rating <= 5
        ):
            errors.append(
                f"Row {row_number}: invalid rating {rating!r}"
            )

        brand = product.get("brand")

        if brand is not None and not isinstance(brand, str):
            errors.append(
                f"Row {row_number}: brand must be text or null"
            )
            
    return errors


def main():
    with INPUT_FILE.open("r", encoding="utf-8") as file:
        products = json.load(file)

    if not isinstance(products, list):
        raise ValueError(
            "Expected the JSON file to contain a list of products."
        )

    errors = validate_products(products)

    print(f"Products checked: {len(products)}")
    print(f"Validation errors: {len(errors)}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")

        raise SystemExit(1)

    print("Validation passed!")


if __name__ == "__main__":
    main()
