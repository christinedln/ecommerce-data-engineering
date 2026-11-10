CREATE TEMP TABLE temp_s3_products_load (
    product_id INTEGER,
    title VARCHAR(500),
    category VARCHAR(500),
    price NUMERIC(12,2),
    stock INTEGER,
    rating NUMERIC(4,2),
    brand VARCHAR(200)
);