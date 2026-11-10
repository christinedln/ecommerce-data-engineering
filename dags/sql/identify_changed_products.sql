
CREATE TEMP TABLE temp_s3_products_changes AS

SELECT source.*
FROM temp_s3_products_load AS source

LEFT JOIN public.raw_products AS target
    ON target.product_id = source.product_id

WHERE target.product_id IS NULL

   OR target.title <> source.title
   OR (target.title IS NULL AND source.title IS NOT NULL)
   OR (target.title IS NOT NULL AND source.title IS NULL)

   OR target.category <> source.category
   OR (target.category IS NULL AND source.category IS NOT NULL)
   OR (target.category IS NOT NULL AND source.category IS NULL)

   OR target.price <> source.price
   OR (target.price IS NULL AND source.price IS NOT NULL)
   OR (target.price IS NOT NULL AND source.price IS NULL)

   OR target.stock <> source.stock
   OR (target.stock IS NULL AND source.stock IS NOT NULL)
   OR (target.stock IS NOT NULL AND source.stock IS NULL)

   OR target.rating <> source.rating
   OR (target.rating IS NULL AND source.rating IS NOT NULL)
   OR (target.rating IS NOT NULL AND source.rating IS NULL)

   OR target.brand <> source.brand
   OR (target.brand IS NULL AND source.brand IS NOT NULL)
   OR (target.brand IS NOT NULL AND source.brand IS NULL);
