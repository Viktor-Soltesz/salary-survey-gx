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
# IMPORTANT: Ensure this matches the name of your expectation suite JSON file
# and the suite referenced in your checkpoint YML if you were using it directly.
# Based on your provided files (csv_schema.warning.json), this should be:
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
# This is the batch_request that includes the actual DataFrame
runtime_batch_request = {
    "datasource_name": DATASOURCE_NAME,
    "data_connector_name": "default_runtime_data_connector_name",
    "data_asset_name": "developer_salaries_csv",  # This should match the data_asset_name used when creating the suite, if applicable
    "runtime_parameters": {"batch_data": df},
    "batch_identifiers": {"default_identifier_name": "csv_batch"},
}

# --- Step 5: Run validation using a dynamic checkpoint ---
print("Running validation checkpoint...")

# Instantiate the Checkpoint without the 'validations' argument in the constructor.
# The 'validations' will be passed to the run() method.
checkpoint = Checkpoint(
    name="csv_schema_checkpoint_runtime",  # You can name this checkpoint as you like
    data_context=context,
    run_name_template='%Y%m%d-%H%M%S-csv-schema-checks', # Optional: can also be in run()
    action_list=[
        {"name": "store_validation_result", "action": {"class_name": "StoreValidationResultAction"}},
        {"name": "store_evaluation_params", "action": {"class_name": "StoreEvaluationParametersAction"}},
        {"name": "update_data_docs", "action": {"class_name": "UpdateDataDocsAction"}},
        # site_names can be specified here if UpdateDataDocsAction needs it and it's fixed
        # e.g., "site_names": ["local_site"] if you always update local_site
        # If empty as in your YML, it updates all sites or default site.
    ]
    # config_version: 1.0, # Optional: if you want to specify it
    # expectation_suite_name: EXPECTATION_SUITE_NAME, # Not here, goes into the validation entry
    # batch_request: {}, # Not here, goes into the validation entry
)

# Run the checkpoint by passing the 'validations' argument.
# This 'validations' list contains the 'batch_request' with the DataFrame.
results = checkpoint.run(
    validations=[
        {
            "batch_request": runtime_batch_request,
            "expectation_suite_name": EXPECTATION_SUITE_NAME, # Use the corrected suite name
            # You can also override action_list per validation if needed:
            # "action_list": [...]
        }
    ]
    # You could also pass other top-level parameters here to override checkpoint's config for this run, e.g.:
    # run_name_template: '%Y%m%d-%H%M%S-my-specific-run',
    # evaluation_parameters: {},
    # runtime_configuration: {},
)

# --- Step 6: Output results and exit appropriately ---
if results.success:
    print("\n✅ CSV schema validation PASSED!")
else:
    print("\n❌ CSV schema validation FAILED!")
    print("\nValidation Results:")
    # print(results) # You might want to print more details from results upon failure

# Optional: Print local link for Data Docs
index_path = os.path.abspath(os.path.join(
    GE_ROOT_DIR, "gx_docs_output", "local_site", "index.html" # Adjusted path for typical Data Docs structure
))
# Ensure data_docs_sites: local_site: base_directory in great_expectations.yml ends with a trailing slash
# e.g. gx_docs_output/ for TupleFilesystemStoreBackend, or if it's gx_docs_output/local_site/
# The default is often gx_root_dir/uncommitted/data_docs/local_site/index.html if not customized heavily.
# Your config has: `base_directory: gx_docs_output/` for `local_site` store_backend
# and `DefaultSiteIndexBuilder`. This typically means `gx_docs_output/index.html` or `gx_docs_output/local_site/index.html`.
# The path provided in your original script `gx_docs_output/index.html` should be correct
# if `local_site` is the only or default site.

# Let's use the path structure from your original script for the Data Docs link as it was working for you.
index_path_original = os.path.abspath(os.path.join(
    GE_ROOT_DIR, "gx_docs_output", "index.html"
))
print(f"\n📄 Data Docs index: file://{index_path_original}")


exit(0 if results.success else 1)