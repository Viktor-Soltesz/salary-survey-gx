import os
import yaml
import json

# Define input and output paths (hardcoded)
yaml_path = "expectation.yaml"
json_dir = "great_expectations/expectations/surveys/developer_salaries"
json_path = os.path.join(json_dir, "warning.json")

# Ensure destination directory exists
os.makedirs(json_dir, exist_ok=True)

# Load the YAML file
with open(yaml_path, "r") as f:
    expectation_data = yaml.safe_load(f)

# Dump to JSON
with open(json_path, "w") as f:
    json.dump(expectation_data, f, indent=2)

print(f"Converted '{yaml_path}' to '{json_path}'")
