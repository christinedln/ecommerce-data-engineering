
SELECT
    product_id,
    stock,
    inventory_attention
FROM {{ ref('inventory_monitoring') }}
WHERE
    (
        stock = 0
        AND inventory_attention != 'out_of_stock'
    )
    OR (
        stock > 0
        AND stock <= 5
        AND inventory_attention != 'low_stock'
    )
    OR (
        stock > 5
        AND inventory_attention != 'adequate_stock'
    )
