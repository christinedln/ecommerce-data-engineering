{{ config(materialized='view') }}

SELECT
    product_id,
    NULLIF(TRIM(title), '') AS title,
    NULLIF(TRIM(category), '') AS category,
    price,
    stock,
    rating,
    NULLIF(TRIM(brand), '') AS brand,
    source_loaded_at
FROM {{ source('ecommerce', 'raw_products') }}