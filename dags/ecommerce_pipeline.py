
from datetime import datetime, timezone

from airflow.sdk import dag, task, get_current_context

from ecommerce.extract_products import extract_and_upload_products
from ecommerce.load_to_redshift import load_products_to_redshift
from ecommerce.run_dbt import run_dbt_build


@dag(
    dag_id="ecommerce_pipeline",
    description="Extract, load, and transform e-commerce product data",
    start_date=datetime(2026, 1, 1, tzinfo=timezone.utc),
    schedule=None,
    catchup=False,
    tags=["ecommerce", "ingestion"],
)
def ecommerce_pipeline():

    @task
    def extract_products():
        context = get_current_context()
        logical_date = context["logical_date"]
        ingestion_date = logical_date.strftime("%Y-%m-%d")

        return extract_and_upload_products(ingestion_date)

    @task
    def load_products(extraction_result):
        return load_products_to_redshift(
            normalized_s3_key=extraction_result["normalized_s3_key"],
            expected_record_count=extraction_result["record_count"],
        )
    
    @task
    def transform_and_test():
        run_dbt_build()

    extraction_result = extract_products()

    load_result = load_products(extraction_result)

    dbt_result = transform_and_test()

    load_result >> dbt_result



ecommerce_pipeline()
