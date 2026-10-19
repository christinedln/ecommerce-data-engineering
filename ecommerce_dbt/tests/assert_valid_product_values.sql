SELECT *
FROM {{ ref('stg_raw_products') }}
WHERE price < 0
   OR stock < 0
   OR rating < 0
   OR rating > 5