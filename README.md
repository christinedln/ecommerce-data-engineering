# E-Commerce Data Engineering Pipeline

A data engineering project that collects e-commerce data from an external API, processes and validates the data, and stores it in a structured PostgreSQL database for analytics.

## Tech Stack

* Python
* PostgreSQL
* SQL
* dbt
* Apache Airflow
* Git/GitHub

## Pipeline

```text
External API
    ↓
Data Ingestion
    ↓
Raw Data
    ↓
Data Validation
    ↓
Transformation
    ↓
PostgreSQL Data Warehouse
    ↓
Analytics-Ready Data
```

## Data Source

Product data is collected from the public DummyJSON API and used for educational and portfolio purposes.