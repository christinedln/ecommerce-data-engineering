
#!/bin/bash

set -e

# Install dbt on the MWAA hybrid component.
if [[ "${MWAA_AIRFLOW_COMPONENT}" != "hybrid" ]]; then
    echo "Skipping dbt installation on ${MWAA_AIRFLOW_COMPONENT}"
    exit 0
fi

echo "Starting dbt environment setup..."

DBT_ENV_DIR="/usr/local/airflow/python3-virtualenv/dbt-env"

echo "Python version:"
python3 --version

# Create the virtual environment if it doesn't exist.
if [[ ! -x "${DBT_ENV_DIR}/bin/python" ]]; then
    sudo mkdir -p "$(dirname "${DBT_ENV_DIR}")"
    sudo python3 -m venv "${DBT_ENV_DIR}"
    sudo chmod -R 777 "${DBT_ENV_DIR}"
fi

# Activate the isolated environment.
source "${DBT_ENV_DIR}/bin/activate"

echo "Installing dbt packages..."

python -m pip install --upgrade --no-cache-dir pip

python -m pip install --no-cache-dir \
    dbt-core==1.12.6 \
    dbt-redshift==1.11.1

echo "Verifying dbt installation..."

dbt --version

deactivate

echo "dbt environment setup completed successfully."
