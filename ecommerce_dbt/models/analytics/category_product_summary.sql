{{ config(materialized='view') }}

SELECT
    category,
    COUNT(*) AS product_count,
    ROUND(AVG(price), 2) AS average_price,
    MIN(price) AS minimum_price,
    MAX(price) AS maximum_price,
    ROUND(AVG(rating), 2) AS average_rating,
    SUM(
        CASE
            WHEN stock_status = 'out_of_stock' THEN 1
            ELSE 0
        END
    ) AS out_of_stock_count
FROM {{ ref('dim_products') }}
GROUP BY category