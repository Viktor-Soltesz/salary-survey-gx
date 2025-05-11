# Data quality tests with Great Expectations for existing tables

This repo is to explore use of [Great Expectations](https://docs.greatexpectations.io/docs/) (GE) to add data quality checks for existing tables.

## Tasks

- [x] Add Dockerfile to run GE CLI
- [ ] Add devcontainer.json for VSCode
- [x] Add expectations
- [ ] Have expectations executed regularly
- [ ] Add scripts to create the SUT table

## How to run validation checkpoint locally

```
make ge/test
```

## Appendix


### How to run GE CLI locally (Docker)

To be inside the container, run:

```
make docker/build

# To enter a container with dataform CLI
make docker/run

# Run great_expectations --version in the container
# The current directry is mounted as /workspaces
```

To run `great_expectations` directly, run:

```
make ge/version
```

### How to run GE CLI locally (VSCode)

1. Open the project in Container
2. Open Terminal to entre the container
3. Run `great_expectations --version`

### How this GE project was created

1. Create a project structure in ge/
```
great_expectations init
```

2. Create a DataSource in ge/
```
great_expectations datasource new --no-jupyter
Using v3 (Batch Request) API

What data would you like Great Expectations to connect to?
    1. Files on a filesystem (for processing with Pandas or Spark)
    2. Relational database (SQL)
: 2

Which database backend are you using?
    1. MySQL
    2. Postgres
    3. Redshift
    4. Snowflake
    5. BigQuery
    6. other - Do you have a working SQLAlchemy connection string?
: 5
To continue editing this Datasource, run jupyter notebook /workspaces/ge/great_expectations/uncommitted/datasource_new.ipynb
```

3. Authenticate Google Cloud API

```
gcloud auth login
```

4. Run Jypiter notebook generated
```
jupyter notebook /workspaces/ge/great_expectations/uncommitted/datasource_new.ipynb --allow-root --ip=0.0.0.0
```

5. Acces the Jypiter notebook with a token at `http://127.0.0.1:8888/?token=<generated-token>`

6. Edit BigQuery details and run cells to save configurations at `http://127.0.0.1:8888/notebooks/datasource_new.ipynb`
```
datasource_name = "my_first_dbt_model"
connection_string = "bigquery://BQ_GCP_PROJECT_ID/dbt_example"
```

When there are no errors, the configurations will be saved in `great_expectations.yml`

7. Shutdown the Jypiter notebook

8. Create a suite by profiling an existing table

```
great_expectations suite new --no-jupyter
Using v3 (Batch Request) API

How would you like to create your Expectation Suite?
    1. Manually, without interacting with a sample batch of data (default)
    2. Interactively, with a sample batch of data
    3. Automatically, using a profiler
: 3

A batch of data is required to edit the suite - let's help you to specify it.


Which data asset (accessible by data connector "default_inferred_data_connector_name") would you like to use?
    1. dataform_assertions.assertion_not_empty
    2. dataform_assertions.assertion_not_null
    3. dbt_example.my_first_dbt_model
    4. dbt_example.my_second_dbt_model

Type [n] to see the next page or [p] for the previous. When you're ready to select an asset, enter the index.
: 3

Name the new Expectation Suite [dbt_example.my_first_dbt_model.warning]:

Great Expectations will create a notebook, containing code cells that select from available columns in your dataset and
generate expectations about them to demonstrate some examples of assertions you can make about your data.

When you run this notebook, Great Expectations will store these expectations in a new Expectation Suite "dbt_example.my_first_dbt_model.warning" here:

  file:///workspaces/ge/great_expectations/expectations/dbt_example/my_first_dbt_model/warning.json

Would you like to proceed? [Y/n]: y
```

9. Run the Jupyter notebook
```
jupyter notebook /workspaces/ge/great_expectations/uncommitted/edit_dbt_example.my_first_dbt_model.warning.ipynb --allow-root --ip=0.0.0.0
```

10. Access the Jupyter notebook with a token at `http://127.0.0.1:8888/?token=<generated token>`

11. Edit and run cells to create expectations at `http://127.0.0.1:8888/notebooks/edit_dbt_example.my_first_dbt_model.warning.ipynb`

Generated expectations will be saved in `expectations/<dataset name>/<table name>/warning.json`

12. Run Validation to create a Checkpoint

```
great_expectations checkpoint new checkpoint_model --no-jupyter
```

13. Run the Jupyter notebook and access it with a token at `http://127.0.0.1:8888/?token=<generated token>`

```
jupyter notebook /workspaces/ge/great_expectations/uncommitted/edit_checkpoint_checkpoint_model.ipynb  --allow-root --ip=0.0.0.0
```

14. Access Data Docs at `http://127.0.0.1:8888/view/data_docs/local_site/index.html`


### References
- Getting Started (official tutorial) https://docs.greatexpectations.io/docs/tutorials/getting_started/tutorial_overview
- Great Expectations Tutorial (official on Github) https://github.com/superconductive/ge_tutorials
- Great Expectations Tutorial https://github.com/datarootsio/tutorial-great-expectations/blob/main/tutorial_great_expectations.ipynb
- How to use Great Expectations https://medium.com/hashmapinc/understanding-great-expectations-and-how-to-use-it-7754c78962f4
- How to use Great Expectations with BigQuery https://medium.com/@Sasakky/how-to-use-great-expectations-with-bigquery-54aad4aa2dd
