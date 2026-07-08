"""
Data Validation in the Mock ML Project :: data validation using the mock ML environment
using conftest.py to define fixtures for reusable mock data:

Shared pytest configuration and fixtures for the PayCare ETL test suite.
"""  # Keep test setup centralized and easy to reuse in CI.

import sys  # Register compatibility aliases for legacy test imports.
from pathlib import Path  # Provide portable filesystem paths for temporary test files.
from types import ModuleType  # Build a lightweight package alias for legacy imports.

import pandas as pd  # Build deterministic DataFrame inputs for ETL tests.
import pytest  # Expose reusable fixtures to every test module in this directory.

# from app import etl as app_etl  # Reuse the real ETL module as the canonical test target.
import app.etl as app_etl  # Import the ETL module so monkeypatching updates the same function object.

# paycare_package = ModuleType("paycare")  # Create a synthetic package name for older test code.
# paycare_package.__path__ = []  # Mark the alias as package-like so submodule imports can resolve.
# paycare_package.etl = app_etl  # Expose app.etl through the expected paycare.etl namespace.
# sys.modules.setdefault("paycare", paycare_package)  # Register the synthetic package only if it is missing.
# sys.modules["paycare.etl"] = app_etl  # Map paycare.etl directly to the real ETL module.


@pytest.fixture(scope="session")  # Create the base dataset once for the whole test session.
def sample_employee_data():  # Share a stable ETL input structure across tests.
	return pd.DataFrame(  # Return a simple, predictable table for extraction and transformation checks.
		{  # Define the sample columns used by the ETL pipeline.
			"name": ["Alice", "Bob", "Charlie"],  # Provide readable sample employee names.
			"salary": [50000, 60000, 70000],  # Use fixed salary values for repeatable tax assertions.
		}  # Close the sample data dictionary.
	)  # Close the DataFrame constructor.


@pytest.fixture(scope="session")  # Build the expected transformed dataset once per test session.
def expected_transformed_data(sample_employee_data):  # Reuse the shared input data to derive the output.
	transformed_data = sample_employee_data.dropna().copy()  # Mirror the ETL cleanup step with an isolated copy.
	transformed_data["tax"] = transformed_data["salary"] * 0.1  # Apply the flat tax rule used by app/etl.py.
	transformed_data["net_salary"] = transformed_data["salary"] - transformed_data["tax"]  # Compute the final salary after tax.
	return transformed_data  # Return the canonical transformed DataFrame for assertions.


@pytest.fixture()  # Create an isolated CSV input file for each test that needs file extraction.
def sample_input_csv(tmp_path, sample_employee_data):  # Use pytest's temporary directory for safe file handling.
	input_file = tmp_path / "input_data.csv"  # Define the temporary input file path.
	sample_employee_data.to_csv(input_file, index=False)  # Persist the sample DataFrame exactly as the ETL expects.
	return input_file  # Return the file path so extract_data can read it.


@pytest.fixture()  # Provide a fresh output path for tests that validate the load step.
def sample_output_csv(tmp_path):  # Reuse pytest's temporary directory to avoid polluting the repository.
	return tmp_path / "output_data.csv"  # Return the path where load_data should write the CSV output.


@pytest.fixture()  # Provide a missing path for negative-path tests without touching real files.
def missing_input_csv(tmp_path):  # Use a temporary location so the path is guaranteed to be isolated.
	return tmp_path / "missing_input_data.csv"  # Return a path that is valid as a Path object but does not exist.


@pytest.fixture()  # Provide an invalid output path for error-handling tests.
def invalid_output_csv(tmp_path):  # Keep the value deterministic and local to the current test session.
	return Path("/invalid_path/output_data.csv")  # Return a path that should fail on CI and local machines.

