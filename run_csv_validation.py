import os
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
# 👇 CORRECTED EXPECTATION SUITE NAME 👇
EXPECTATION_SUITE_NAME = "surveys/developer_salaries/csv_schema_warning"
DATASOURCE_NAME = "my_pandas_datasource"

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

# --- Step 4: Define RuntimeBatchRequest ---
print("Creating RuntimeBatchRequest for CSV data...")
runtime_batch_request = {
    "datasource_name": DATASOURCE_NAME,
    "data_connector_name": "default_runtime_data_connector_name",
    "data_asset_name": "developer_salaries_csv", # This should match the data_asset_name used when the suite was created or is intended for.
    "runtime_parameters": {"batch_data": df},
    "batch_identifiers": {"default_identifier_name": "csv_batch"},
}

# Define the action list once
ACTIONS_FOR_VALIDATION = [
    {"name": "store_validation_result", "action": {"class_name": "StoreValidationResultAction"}},
    {"name": "store_evaluation_params", "action": {"class_name": "StoreEvaluationParametersAction"}},
    {"name": "update_data_docs", "action": {"class_name": "UpdateDataDocsAction"}},
]

# --- Step 5: Run validation using a dynamic checkpoint ---
print("Running validation checkpoint...")

checkpoint = Checkpoint(
    name="csv_schema_checkpoint_runtime", # This is a runtime name for the checkpoint object
    data_context=context,
    run_name_template='%Y%m%d-%H%M%S-csv-schema-checks',
)

results = checkpoint.run(
    validations=[
        {
            "batch_request": runtime_batch_request,
            "expectation_suite_name": EXPECTATION_SUITE_NAME,
            "action_list": ACTIONS_FOR_VALIDATION,
        }
    ]
)

# --- Step 6: Output results and exit appropriately ---
if results.success:
    print("\n✅ CSV schema validation PASSED!")
else:
    print("\n❌ CSV schema validation FAILED!")
    # Optional: print more details about failures
    # for validation_result_identifier in results.list_validation_result_identifiers():
    #     validation_result = results.get_validation_result(validation_result_identifier)
    #     print(f"Validation for suite {validation_result.meta.get('expectation_suite_name')} failed:")
    #     for expectation_result in validation_result.results:
    #         if not expectation_result.success:
    #             print(f"  Expectation: {expectation_result.expectation_config.expectation_type}")
    #             print(f"  Result: {expectation_result.result}")


index_path_original = os.path.abspath(os.path.join(
    GE_ROOT_DIR, "gx_docs_output", "index.html"
))
print(f"\n📄 Data Docs index: file://{index_path_original}")

exit(0 if results.success else 1)