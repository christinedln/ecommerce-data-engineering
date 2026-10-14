# E-Commerce Data Engineering Pipeline

A data engineering portfolio project that collects e-commerce product data from a public API, prepares it for ingestion, stores raw data in Amazon S3, and loads structured records into Amazon Redshift for analytics.

## Tech Stack

* Python – API ingestion and data preparation
* Amazon S3 – Cloud object storage for raw and prepared data
* Amazon Redshift Serverless – Cloud data warehouse
* SQL – Data loading, validation, and troubleshooting

## Pipeline

```text
External API
    ↓
Data Ingestion
    ↓
Raw Data Storage
    ↓
Data Processing
    ↓
Data Warehouse
    ↓
Analytics-Ready Data
```

## Data Source

Product data is collected from the public DummyJSON API and used for educational and portfolio purposes.