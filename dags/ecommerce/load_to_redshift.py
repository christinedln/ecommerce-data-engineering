
import time
from pathlib import Path

import boto3


AWS_REGION = "us-east-1"
REDSHIFT_WORKGROUP = "ecommerce-workgroup"
REDSHIFT_DATABASE = "dev"

S3_BUCKET = "ecommerce-data-engineering-878093321287-us-east-1-an"

REDSHIFT_S3_ROLE = (
    "arn:aws:iam::878093321287:role/"
    "RedshiftS3ProductsReadRole"
)


def wait_for_statement(redshift_data, statement_id):
    """Wait until a Redshift Data API statement finishes."""

    while True:
        response = redshift_data.describe_statement(
            Id=statement_id
        )

        status = response["Status"]

        if status == "FINISHED":
            return response

        if status in ("FAILED", "ABORTED"):
            raise RuntimeError(
                f"Redshift statement {status}: "
                f"{response.get('Error', 'Unknown error')}"
            )

        time.sleep(2)



def execute_sql(
    redshift_data,
    sql,
    session_id=None,
    keep_alive=3600
):
    """Execute SQL and preserve the Redshift session."""

    parameters = {
        "Sql": sql,
        "SessionKeepAliveSeconds": keep_alive,
    }

    # First request: establish a new Redshift session
    if session_id is None:
        parameters["Database"] = REDSHIFT_DATABASE
        parameters["WorkgroupName"] = REDSHIFT_WORKGROUP

    # Subsequent requests: reuse the existing session
    else:
        parameters["SessionId"] = session_id

    response = redshift_data.execute_statement(**parameters)

    wait_for_statement(
        redshift_data,
        response["Id"]
    )

    return response


def load_products_to_redshift(
    normalized_s3_key,
    expected_record_count
):
    """Load normalized product data from S3 into Redshift staging."""

    redshift_data = boto3.client(
        "redshift-data",
        region_name=AWS_REGION
    )

    # 1. Read the staging table SQL file
    sql_file = (
        Path(__file__).resolve().parents[1]
        / "sql"
        / "create_staging_table.sql"
    )

    create_table_sql = sql_file.read_text(
        encoding="utf-8"
    )

    # 2. Create the temporary staging table
    create_response = execute_sql(
        redshift_data,
        create_table_sql
    )

    session_id = create_response["SessionId"]

    # 3. Load normalized JSONL data from S3
    s3_uri = f"s3://{S3_BUCKET}/{normalized_s3_key}"

    copy_sql = f"""
        COPY temp_s3_products_load
        (
            product_id,
            title,
            category,
            price,
            stock,
            rating,
            brand
        )
        FROM '{s3_uri}'
        IAM_ROLE '{REDSHIFT_S3_ROLE}'
        FORMAT AS JSON 'auto';
    """

    execute_sql(
        redshift_data,
        copy_sql,
        session_id=session_id
    )

    # 4. Verify the number of loaded records
    count_response = execute_sql(
        redshift_data,
        """
        SELECT COUNT(*) AS total_records
        FROM temp_s3_products_load;
        """,
        session_id=session_id
    )

    result = redshift_data.get_statement_result(
        Id=count_response["Id"]
    )

    actual_record_count = (
        result["Records"][0][0]["longValue"]
    )

    if actual_record_count != expected_record_count:
        raise ValueError(
            f"Expected {expected_record_count} records, "
            f"but loaded {actual_record_count}"
        )
    
    print(
        f"Successfully loaded {actual_record_count} "
        "products into Redshift staging."
    )
    
    # 5. Check for duplicate product IDs
    duplicate_response = execute_sql(
        redshift_data,
        """
        SELECT COUNT(*)
        FROM (
            SELECT product_id
            FROM temp_s3_products_load
            GROUP BY product_id
            HAVING COUNT(*) > 1
        ) duplicates;
        """,
        session_id=session_id
    )

    duplicate_result = redshift_data.get_statement_result(
        Id=duplicate_response["Id"]
    )

    duplicate_count = (
        duplicate_result["Records"][0][0]["longValue"]
    )

    if duplicate_count > 0:
        raise ValueError(
            f"Found {duplicate_count} duplicate product IDs"
        )

    # 6. Check for missing required fields
    missing_response = execute_sql(
        redshift_data,
        """
        SELECT COUNT(*)
        FROM temp_s3_products_load
        WHERE product_id IS NULL
           OR title IS NULL
           OR TRIM(title) = ''
           OR category IS NULL
           OR TRIM(category) = '';
        """,
        session_id=session_id
    )

    missing_result = redshift_data.get_statement_result(
        Id=missing_response["Id"]
    )

    missing_count = (
        missing_result["Records"][0][0]["longValue"]
    )

    if missing_count > 0:
        raise ValueError(
            f"Found {missing_count} records with missing "
            "required fields"
        )

    print("Data quality validation successful!")
    print(f"Duplicate product ID groups: {duplicate_count}")
    print(f"Records with missing required fields: {missing_count}")

    
    # 7. Identify new and changed products
    changes_sql_file = (
        Path(__file__).resolve().parents[1]
        / "sql"
        / "identify_changed_products.sql"
    )

    changes_sql = changes_sql_file.read_text(
        encoding="utf-8"
    )

    execute_sql(
        redshift_data,
        changes_sql,
        session_id=session_id
    )

    # 8. Count new and changed products
    changes_count_response = execute_sql(
        redshift_data,
        """
        SELECT COUNT(*)
        FROM temp_s3_products_changes;
        """,
        session_id=session_id
    )

    changes_result = redshift_data.get_statement_result(
        Id=changes_count_response["Id"]
    )

    changes_count = (
        changes_result["Records"][0][0]["longValue"]
    )

    print(
        f"New or changed products detected: {changes_count}"
    )

    # 9. Read the merge SQL file
    merge_sql_file = (
        Path(__file__).resolve().parents[1]
        / "sql"
        / "merge_products.sql"
    )

    merge_sql = merge_sql_file.read_text(
        encoding="utf-8"
    )

    # 10. Merge new and changed products
    execute_sql(
        redshift_data,
        merge_sql,
        session_id=session_id
    )

    print("Successfully executed product merge.")


    # 11. Verify the target table record count
    target_count_response = execute_sql(
        redshift_data,
        """
        SELECT COUNT(*)
        FROM public.raw_products;
        """,
        session_id=session_id
    )

    target_result = redshift_data.get_statement_result(
        Id=target_count_response["Id"]
    )

    target_record_count = (
        target_result["Records"][0][0]["longValue"]
    )

    print(
        f"Total records in public.raw_products: "
        f"{target_record_count}"
    )

    return {
        "session_id": session_id,
        "record_count": actual_record_count,
        "target_record_count": target_record_count,
    }



def test_redshift_connection():
    """Test Redshift Data API access using the MWAA execution role."""

    redshift_data = boto3.client(
        "redshift-data",
        region_name=AWS_REGION
    )

    response = execute_sql(
        redshift_data,
        "SELECT current_user, current_database();"
    )

    result = redshift_data.get_statement_result(
        Id=response["Id"]
    )

    row = result["Records"][0]

    db_user = row[0]["stringValue"]
    database = row[1]["stringValue"]

    print("Redshift connection successful!")
    print(f"Database user: {db_user}")
    print(f"Database: {database}")

    return {
        "db_user": db_user,
        "database": database,
    }
