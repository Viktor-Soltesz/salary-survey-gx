import great_expectations as gx
context = gx.get_context()          # or DataContext(...)
suite = context.get_expectation_suite(
    "surveys.developer_salaries.csv_schema_warning"
)
context.add_or_update_expectation_suite(suite)
