
from pathlib import Path
import shutil
import subprocess


DBT_EXECUTABLE = (
    "/usr/local/airflow/python3-virtualenv/dbt-env/bin/dbt"
)

DAGS_DBT_DIR = Path("/usr/local/airflow/dags/dbt")
WORKING_DIR = Path("/tmp/dbt")


def run_dbt_build():
    """
    Copy the dbt project to a writable directory
    and execute dbt transformations and data quality tests.
    """

    # Remove files from a previous execution.
    if WORKING_DIR.exists():
        shutil.rmtree(WORKING_DIR)

    # Copy the dbt project and profiles.yml from the MWAA DAG directory.
    shutil.copytree(DAGS_DBT_DIR, WORKING_DIR)

    # Execute dbt build.
    command = [
        DBT_EXECUTABLE,
        "build",
        "--project-dir",
        str(WORKING_DIR / "ecommerce_dbt"),
        "--profiles-dir",
        str(WORKING_DIR),
    ]

    subprocess.run(command, check=True)
