
WITH source_counts AS (
    SELECT COUNT(*) AS total_products
    FROM {{ ref('dim_products') }}
),

summary_counts AS (
    SELECT SUM(product_count) AS total_products
    FROM {{ ref('category_product_summary') }}
)

SELECT
    source_counts.total_products AS source_total,
    summary_counts.total_products AS summary_total
FROM source_counts
CROSS JOIN summary_counts
WHERE source_counts.total_products
      <> summary_counts.total_products
