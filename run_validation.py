import great_expectations as gx
import os

# Define the path to your great_expectations directory relative to this script
# Assuming run_validation.py is in the directory *above* the 'ge' folder
GE_ROOT_DIR = "ge/great_expectations"

# Define the name of the checkpoint you want to run
CHECKPOINT_NAME = "checkpoint_model"

print(f"Loading Great Expectations DataContext from: {GE_ROOT_DIR}")

try:
    # Instantiate the DataContext
    # In V0, the DataContext is loaded by specifying the root directory.
    context = gx.DataContext(context_root_dir=GE_ROOT_DIR)
    print("DataContext loaded successfully.")

except Exception as e:
    print(f"Error loading DataContext: {e}")
    print("Please ensure the GE_ROOT_DIR is correct and great_expectations.yml exists.")
    exit(1) # Exit if DataContext cannot be loaded

print(f"Getting Checkpoint: {CHECKPOINT_NAME}")

try:
    # Get the checkpoint by name from the DataContext
    checkpoint = context.get_checkpoint(name=CHECKPOINT_NAME)
    print("Checkpoint loaded successfully.")

except Exception as e:
    print(f"Error getting Checkpoint '{CHECKPOINT_NAME}': {e}")
    print("Please ensure 'checkpoints/checkpoint_model.yml' exists and is correctly configured.")
    exit(1) # Exit if Checkpoint cannot be loaded


print(f"Running Checkpoint: {CHECKPOINT_NAME}")

try:
    # Run the checkpoint
    # The run() method executes the validations defined in the checkpoint
    results = checkpoint.run()
    print("Checkpoint run finished.")

except Exception as e:
    print(f"An error occurred during Checkpoint execution: {e}")
    # This could happen due to connection issues, configuration problems, etc.
    exit(1)


# Process the results
if results.success:
    print("\n Great Expectations Checkpoint run PASSED!")
    # You can access detailed results if needed, e.g., results.run_results
else:
    print("\n Great Expectations Checkpoint run FAILED!")
    # You might want to inspect results.run_results for details on failures
    # print("Failure details:", results) # Uncomment for verbose output


# Optionally, provide a link to the generated Data Docs
# Based on your great_expectations.yml, data docs are stored locally
data_docs_path_relative = os.path.join(GE_ROOT_DIR, "uncommitted", "data_docs", "local_site", "index.html")
data_docs_path_absolute = os.path.abspath(data_docs_path_relative)

if os.path.exists(data_docs_path_absolute):
     print(f"\nView detailed results in Data Docs: file://{data_docs_path_absolute}")
else:
     print("\nData Docs index.html not found. Check your great_expectations.yml and the actions in your checkpoint.")


# Exit with a status code reflecting success or failure
if results.success:
    exit(0) # Success
else:
    exit(1) # Failure