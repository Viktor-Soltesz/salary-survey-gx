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
EXPECTATION_SUITE_NAME = "csv_schema.warning"  # Corrected to match your JSON file name
DATASOURCE_NAME = "my_pandas_datasource"
CHECKPOINT_NAME = "csv_schema_checkpoint" # Added checkpoint name

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

# --- Step 4: Define RuntimeBatchRequest (without batch_data) ---
# This defines the structure for the batch request that the checkpoint expects.
# The actual batch_data is passed at runtime when calling checkpoint.run().
base_batch_request = {
    "datasource_name": DATASOURCE_NAME,
    "data_connector_name": "default_runtime_data_connector_name",
    "data_asset_name": "developer_salaries_csv",
    "batch_identifiers": {"default_identifier_name": "csv_batch"},
}

# --- Step 5: Run validation using the pre-configured checkpoint ---
print("Running validation checkpoint...")

# Get the checkpoint by name from the DataContext
checkpoint = context.get_checkpoint(name=CHECKPOINT_NAME)

# Prepare the batch request with the actual DataFrame for running the checkpoint
runtime_batch_request_with_data = base_batch_request.copy()
runtime_batch_request_with_data["runtime_parameters"] = {"batch_data": df}


results = checkpoint.run(
    validations=[
        {
            "batch_request": runtime_batch_request_with_data,
            "expectation_suite_name": EXPECTATION_SUITE_NAME,
        }
    ]
)

# --- Step 6: Output results and exit appropriately ---
if results.success:
    print("\n✅ CSV schema validation PASSED!")
else:
    print("\n❌ CSV schema validation FAILED!")

# Optional: Print local link for Data Docs (in Docker, not usable but good locally)
index_path = os.path.abspath(os.path.join(
    GE_ROOT_DIR, "gx_docs_output", "index.html"
))
print(f"\n📄 Data Docs index: file://{index_path}")

exit(0 if results.success else 1)