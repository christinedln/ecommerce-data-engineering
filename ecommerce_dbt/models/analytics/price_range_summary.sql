
{{ config(materialized='view') }}

WITH products_with_price_range AS (
    SELECT
        product_id,
        price,
        CASE
            WHEN price < 50 THEN 'under_50'
            WHEN price < 100 THEN '50_to_99_99'
            WHEN price < 500 THEN '100_to_499_99'
            ELSE '500_and_above'
        END AS price_range
    FROM {{ ref('dim_products') }}
)

SELECT
    price_range,
    COUNT(*) AS product_count,
    ROUND(
        COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (),
        2
    ) AS percentage_of_products
FROM products_with_price_range
GROUP BY price_range
