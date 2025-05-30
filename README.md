# salary-survey-gx

## Data Quality Monitoring (Stage 5 of 6)

This repository integrates **Great Expectations (GX)** into the ELT pipeline as a **non-blocking data quality monitor**.  
It performs pre- and post-transformation validations on survey data stored in BigQuery — offering observability over schema consistency, value distributions, and expectations compliance across runs.

GX is run in *observer mode*: failing expectations do **not block** the pipeline, but are logged and published for review. This complements model-level monitoring handled by Elementary.

---

## Project Overview

This project is split into modular repositories, each handling one part of the full ELT and analytics pipeline:

| Stage | Name                        | Description                                | Repository |
|-------|-----------------------------|--------------------------------------------|------------|
| 1     | Ingestion & Infrastructure  | Terraform + Cloud Functions for ETL        | [salary-survey-iac](https://github.com/Viktor-Soltesz/salary-survey-iac) |
| 2     | Modeling & Transformation   | DBT models, metrics, testing               | [salary-survey-dbt](https://github.com/Viktor-Soltesz/salary-survey-dbt) |
| 3     | Business Intelligence       | Tableau dashboards                         | Tableau Public |
| 4     | Model Observability         | Drift & lineage tracking (Elementary)      | [salary-survey-edr](https://github.com/Viktor-Soltesz/salary-survey-edr) |
| 5     | **Data Quality Monitoring** | GX expectations before/after DBT           | **[salary-survey-gx](https://github.com/Viktor-Soltesz/salary-survey-gx)** |
| 6     | Statistical Analysis        | ANOVA, regressions, prediction             | [salary-analysis](https://github.com/Viktor-Soltesz/salary-analysis) |

---

## Repository Scope

This repository configures and runs Great Expectations to:
- Validate schema, ranges, distributions, and nulls
- Detect drift or anomalies between runs
- Log and publish validation results for review
- Provide insight into pipeline reliability at both raw and transformed stages

Validations are configured against:
- **Pre-DBT input tables** (e.g., staged cleaned CSVs)
- **Post-DBT output tables** (e.g., final marts)

---

## Detailed Breakdown

### 1. Validation Strategy

- **Pre-DBT Validations**:
  - Validate incoming data right after ingestion and staging
  - Expectations include column presence, value ranges, null rates, and types

- **Post-DBT Validations**:
  - Run against final marts to validate business logic integrity
  - Expectations monitor computed columns, categorical values, normalized salaries, etc.

---

### 2. Great Expectations Features

- **Data Context** stored locally in the repo
- **Batch requests** connect to BigQuery via service account
- **Expectation suites** defined per table
- **Checkpoints** run via CLI or GitHub Actions
- **Validation results** are stored and optionally rendered to GitHub Pages

---

### 3. GitHub Actions Integration

- GX runs triggered after:
  - Raw data ingestion
  - DBT model completion
- Docker-based environment for reproducibility
- Output includes:
  - Validation summary (pass/fail counts)
  - Rendered HTML reports (committed or published)

---

### 4. Publishing & Reporting

- Validation results saved to disk and/or committed
- GitHub Pages optionally used to serve rendered expectations
- All expectation suites and validation reports version-controlled in Git

---

## Setup Instructions

1. Clone this repo and install Great Expectations:
   ```bash
   pip install great_expectations
