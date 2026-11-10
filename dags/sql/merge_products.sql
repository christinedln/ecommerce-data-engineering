
MERGE INTO public.raw_products
USING temp_s3_products_changes AS source
ON public.raw_products.product_id = source.product_id

WHEN MATCHED THEN UPDATE SET
    title = source.title,
    category = source.category,
    price = source.price,
    stock = source.stock,
    rating = source.rating,
    brand = source.brand,
    source_loaded_at = GETDATE()

WHEN NOT MATCHED THEN INSERT (
    product_id,
    title,
    category,
    price,
    stock,
    rating,
    brand
)
VALUES (
    source.product_id,
    source.title,
    source.category,
    source.price,
    source.stock,
    source.rating,
    source.brand
);
