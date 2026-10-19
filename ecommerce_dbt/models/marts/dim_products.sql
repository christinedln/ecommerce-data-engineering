{{ config(materialized='table') }}

SELECT
    product_id,
    title,
    category,
    price,
    stock,
    rating,
    brand,
    CASE
        WHEN stock > 0 THEN 'in_stock'
        WHEN stock = 0 THEN 'out_of_stock'
    END AS stock_status,
    source_loaded_at
FROM {{ ref('stg_raw_products') }}