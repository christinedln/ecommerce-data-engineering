SELECT
    product_id,
    title,
    category,
    stock,
    stock_status,
    CASE
        WHEN stock = 0 THEN 'out_of_stock'
        WHEN stock <= 5 THEN 'low_stock'
        ELSE 'adequate stock'
    END AS inventory_attention
FROM {{ ref('dim_products') }}