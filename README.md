# Data Observability (Stage 3 of 5)

This repository integrates **Great Expectations (GX)** into the ELT pipeline as a **non-blocking data quality monitor**.  
It performs pre- and post-transformation validations on survey data stored in BigQuery — offering observability over schema consistency, value distributions, and expectations compliance across runs.

GX is run in *observer mode*: failing expectations do **not block** the pipeline, but are logged and published for review. This complements model-level monitoring handled by Elementary.

---

## Project Overview

This project is split into modular repositories, each handling one part of the full ELT and analytics pipeline:

| Stage | Name                        | Description                                | Link |
|-------|-----------------------------|--------------------------------------------|------------|
| ㅤ1     | Ingestion & Infrastructure  | Terraform + Python Cloud Functions        | [salary-survey-iac (GitHub)](https://github.com/Viktor-Soltesz/salary-survey-iac) |
| ㅤ2     | Data Transformation   | DBT data models and testing               | [salary-survey-dbt (GitHub)](https://github.com/Viktor-Soltesz/salary-survey-dbt) <br> ㅤ⤷ [DBT docs](https://viktor-soltesz.github.io/salary-survey-dbt-docs/index.html#!/overview)|
| **▶️3** | **Data Observability**  | **Great Expectations & Elementary,** <br> **model monitoring and data observability**     | **[salary-survey-gx (GitHub)](https://github.com/Viktor-Soltesz/salary-survey-gx)** <br> ㅤ⤷ **[GX log](https://viktor-soltesz.github.io/salary-survey-gx/gx_site/index.html)** <br> ㅤ⤷ **[Elementary report](https://viktor-soltesz.github.io/salary-survey-dbt/elementary_report.html#/report/dashboard)** |
| ㅤ4     | Statistical Modeling    | ANOVA, multiregressions, prediction   | [salary-survey-analysis (GitHub)](https://github.com/Viktor-Soltesz/salary-survey-analysis) |
| ㅤ5     | Dashboards          | •ㅤInteractive salary exploration <br> •ㅤData Health metrics (from DBT) <br> •ㅤBilling report (from GCP invoicing) <br> •ㅤBigQuery report (from GCP logging) |ㅤ🡢 [Tableau Public](https://public.tableau.com/app/profile/viktor.solt.sz/viz/SoftwareDeveloperSalaries/Dashboard) <br>ㅤ🡢 [Looker Studio](https://lookerstudio.google.com/s/mhwL6JfNlaw)<br>ㅤ🡢 [Looker Studio](https://lookerstudio.google.com/s/tp8jUo4oPRs)<br>ㅤ🡢 [Looker Studio](https://lookerstudio.google.com/s/v2BIFW-_Jak)|
| ㅤ+     | Extra material | •ㅤPresentation <br> •ㅤData Dictionary <br>  •ㅤSLA Table <br>  •ㅤMy LinkedIn<br>  •ㅤMy CV|ㅤ🡢 [Google Slides](https://docs.google.com/presentation/d/1BHC6QnSpObVpulEcyDLXkW-6YLo2hpnwQ3miQg43iBg/edit?slide=id.g3353e8463a7_0_28#slide=id.g3353e8463a7_0_28) <br>ㅤ🡢 [Google Sheets](https://docs.google.com/spreadsheets/d/1cTikHNzcw3e-gH3N8F4VX-viYlCeLbm5JkFE3Wdcnjo/edit?gid=0#gid=0) <br>ㅤ🡢 [Google Sheets](https://docs.google.com/spreadsheets/d/1r85NlwsGV1DDy4eRBfMjZgI-1_uyIbl1fUazgY00Kz0/edit?usp=sharing) <br>ㅤ🡢 [LinkedIn](https://www.linkedin.com/in/viktor-soltesz/) <br>ㅤ🡢 [Google Docs](https://www.linkedin.com/in/viktor-soltesz/)|

---

## Repository Scope

### Great Expectations

This repo uses **GX as the main tool** to:
- Monitor schema, value distributions, and nulls
- Catch data drift and anomalies across time
- Validate data **before and after GCP pipeline**
- Run in **observer mode** (failures are reported, but not pipeline-blocking)
- Log and publish rich validation reports for audit and review.

### Elementary

Elementary runs **after DBT** to:
- Track test performance and data freshness
- Visualize model-level lineage and historical changes
- Publish dashboards and test run summaries
- Provide non-blocking observability from within the DBT ecosystem

---

## Detailed Breakdown

### 1. GX Validation Strategy

- **Pre-DBT Validations**:
  - Run on cleaned/staged raw data
  - Expectation suites validate: schema, types, ranges, nulls, duplicates

- **Post-DBT Validations**:
  - Run on final marts (e.g. normalized salary tables)
  - Validate computed columns, outlier removal, categorical consistency

---

### 2. Great Expectations Features

- **Local data context** stored in the repo
- **Batch requests** connect to BigQuery via service account
- **Expectation suites** per table and stage
- **Checkpoints** for automated test execution
- **Validation results**:
  - Saved locally and optionally rendered
  - Can be published to GitHub Pages

---

### 3. Elementary Observability (DBT Layer)

- **Lineage Graph**: visualize model dependencies
- **Test Monitoring**: track failures, flaky tests
- **Freshness Checks**: detect stale or missing updates
- **Schema Change Detection**: flag renamed or removed columns
- **Run History**: show model build time and status

---

### 4. GitHub Actions Integration

- **GX**
  - Triggered after raw ingestion and DBT runs
  - Runs in Dockerized CI environment
  - Outputs:
    - Validation pass/fail logs
    - Rendered HTML reports
- **Elementary**
  - Runs after `dbt run`
  - Outputs:
    - Observability dashboards
    - Lineage metadata and test summaries
  - Published to `gh-pages` for browser-based review
