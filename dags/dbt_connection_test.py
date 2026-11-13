
from datetime import datetime, timezone
from pathlib import Path
import shutil
import subprocess

from airflow.sdk import dag, task


DBT_EXECUTABLE = (
    "/usr/local/airflow/python3-virtualenv/dbt-env/bin/dbt"
)

DAGS_DBT_DIR = Path("/usr/local/airflow/dags/dbt")
WORKING_DIR = Path("/tmp/dbt")


@dag(
    dag_id="dbt_connection_test",
    description="Test dbt installation and Redshift connection",
    start_date=datetime(2026, 1, 1, tzinfo=timezone.utc),
    schedule=None,
    catchup=False,
    tags=["dbt", "testing"],
)
def dbt_connection_test():

    @task
    def run_dbt_debug():

        # Remove any files left by a previous test.
        if WORKING_DIR.exists():
            shutil.rmtree(WORKING_DIR)

        # Copy the dbt project and profiles.yml to a writable directory.
        shutil.copytree(DAGS_DBT_DIR, WORKING_DIR)

        # Test the dbt project configuration and Redshift connection.
        command = [
            DBT_EXECUTABLE,
            "debug",
            "--project-dir",
            str(WORKING_DIR / "ecommerce_dbt"),
            "--profiles-dir",
            str(WORKING_DIR),
        ]

        subprocess.run(command, check=True)


    run_dbt_debug()


dbt_connection_test()
