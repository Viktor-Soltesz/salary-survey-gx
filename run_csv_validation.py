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
EXPECTATION_SUITE_NAME = "csv_schema.warning"
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
    "data_asset_name": "developer_salaries_csv",
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

# Instantiate the Checkpoint with a name.
# We don't need to pass the action_list here if we pass it with each validation below
# OR, you can pass it here as a default for *all* validations if you don't override.
# However, the error suggests it needs to be present with the validation dict.
checkpoint = Checkpoint(
    name="csv_schema_checkpoint_runtime",
    data_context=context,
    run_name_template='%Y%m%d-%H%M%S-csv-schema-checks',
    # You can keep action_list here if you intend it to be a default for all validations
    # that don't explicitly specify their own action_list.
    # But for now, we'll explicitly pass it to the validation dict in run().
    # action_list=ACTIONS_FOR_VALIDATION, # Removed from here to demonstrate explicit per-validation list
)

# Run the checkpoint by passing the 'validations' argument,
# ensuring each validation entry has an 'action_list'.
results = checkpoint.run(
    validations=[
        {
            "batch_request": runtime_batch_request,
            "expectation_suite_name": EXPECTATION_SUITE_NAME,
            "action_list": ACTIONS_FOR_VALIDATION, # <-- ADDED HERE!
        }
    ]
)

# --- Step 6: Output results and exit appropriately ---
if results.success:
    print("\n✅ CSV schema validation PASSED!")
else:
    print("\n❌ CSV schema validation FAILED!")
    print("\nValidation Results:")
    # You can iterate through results to get more specific failure reasons
    # for result in results.list_validation_results():
    #     if not result.success:
    #         print(f"  Validation for suite {result.meta.get('expectation_suite_name')} failed.")
    #         for expectation_result in result.results:
    #             if not expectation_result.success:
    #                 print(f"    Expectation: {expectation_result.expectation_config.expectation_type}")
    #                 print(f"    Result: {expectation_result.result}")


index_path_original = os.path.abspath(os.path.join(
    GE_ROOT_DIR, "gx_docs_output", "index.html"
))
print(f"\n📄 Data Docs index: file://{index_path_original}")

exit(0 if results.success else 1)
