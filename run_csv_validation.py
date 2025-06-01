import os
from datetime import datetime
import pandas as pd
import great_expectations as gx
from google.cloud import storage
from great_expectations.checkpoint import Checkpoint

# --- Configuration ---
PROJECT_ID = "software-developer-salaries"
BUCKET_NAME = "software-developer-salaries-upload"
BLOB_PATH = "surveys/developer_salaries/ai-jobsnet_salaries_2024.csv"
LOCAL_CSV_PATH = "/tmp/developer_salaries.csv"

GE_ROOT_DIR = "great_expectations"
EXPECTATION_SUITE_NAME = "surveys.developer_salaries.csv_schema_warning"
DATASOURCE_NAME = "my_pandas_datasource"

# --- Status Initialization ---
status = "unknown"

try:
    # --- Step 1: Download CSV from GCS ---
    print("Downloading CSV from GCS...")
    client = storage.Client(project=PROJECT_ID)
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(BLOB_PATH)
    blob.download_to_filename(LOCAL_CSV_PATH)
    print(f"Downloaded: gs://{BUCKET_NAME}/{BLOB_PATH} → {LOCAL_CSV_PATH}")

    # --- Step 2: Load CSV with pandas ---
    print("Loading CSV into DataFrame...")
    df = pd.read_csv(LOCAL_CSV_PATH)

    # --- Step 3: Load GX DataContext ---
    print(f"Loading Great Expectations context from: {GE_ROOT_DIR}")
    context = gx.DataContext(context_root_dir=GE_ROOT_DIR)

    try:
        context.get_expectation_suite(EXPECTATION_SUITE_NAME)
    except gx.exceptions.DataContextError:
        raise RuntimeError(
            f"Expectation suite '{EXPECTATION_SUITE_NAME}' not found. Make sure its saved under great_expectations/expectations/..."
        )

    # --- Step 4: Define RuntimeBatchRequest ---
    print("Creating RuntimeBatchRequest for CSV data...")
    runtime_batch_request = {
        "datasource_name": DATASOURCE_NAME,
        "data_connector_name": "default_runtime_data_connector_name",
        "data_asset_name": "developer_salaries_csv",
        "runtime_parameters": {"batch_data": df},
        "batch_identifiers": {"default_identifier_name": "csv_batch"},
    }

    # --- Step 5: Run validation using a dynamic checkpoint ---
    print("Running validation checkpoint...")
    checkpoint = Checkpoint(
        name="csv_schema_checkpoint_runtime",
        data_context=context,
        run_name_template='%Y%m%d-%H%M%S-csv-schema-checks',
    )

    run_name = datetime.utcnow().strftime("%Y%m%d-%H%M%S-csv-schema-checks")

    results = checkpoint.run(
        run_name=run_name,
        validations=[
            {
                "batch_request": runtime_batch_request,
                "expectation_suite_name": EXPECTATION_SUITE_NAME,
                "action_list": [
                    {"name": "store_validation_result", "action": {"class_name": "StoreValidationResultAction"}},
                    {"name": "store_evaluation_params", "action": {"class_name": "StoreEvaluationParametersAction"}},
                    {"name": "update_data_docs", "action": {"class_name": "UpdateDataDocsAction"}},
                ],
            }
        ]
    )

    context.build_data_docs()

    if results.success:
        status = "validation_passed"
        print("\n Run success, CSV schema validation PASSED!")
    else:
        status = "validation_failed"
        print("\n Run success, CSV schema validation FAILED!")

except Exception as e:
    status = "script_failed"
    print(f"\n Script run failed: {e}")

finally:
    with open("gx_status.txt", "w", encoding="utf-8") as f:
        f.write(status)

    index_path_original = os.path.abspath(os.path.join(
        GE_ROOT_DIR, "gx_docs_output", "index.html"
    ))
    print(f"\n Data Docs index: file://{index_path_original}")

    # Exit with 0 so GHA completes and Slack jobs can conditionally run
    exit(0)
