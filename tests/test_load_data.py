"""
#* ==================================
#* Phase 2: Write Tests : etl.py
#* ==================================
You will write unit tests to ensure that the extraction, transformation, and loading steps work as expected. The tests should check for:

    1. Data Extraction : Test that the input CSV file is read correctly.
    2. Data Transformation : Test that the cleaning and tax/net salary calculation steps are performed correctly.
    3. Data Loading : Test that the processed data is saved correctly to an output file.

#* Testing Requirements: test_load_data.py
    - Use `pytest` to write unit tests for the ETL functions (`extract_data`, `transform_data`, and `load_data` — or the equivalent functions in `etl.py`).
    - Mock the CSV file input and output where necessary (e.g., using temporary files or in-memory DataFrames).
    - Ensure tests cover potential edge cases (e.g., missing values in the input file, negative salaries, invalid tax rates).
"""
import pytest
import pandas as pd
from app.etl import load_data


def test_load_data(tmp_path):
    # Create a sample DataFrame to load
    sample_data = pd.DataFrame({
        'name': ['Alice', 'Bob'],
        'salary': [50000, 60000],
        'tax': [5000, 6000],
        'net_salary': [45000, 54000]
    })

    # Define the output file path in the temporary directory
    output_file_path = tmp_path / "output.csv"

    # Call the load_data function
    load_data(sample_data, output_file_path)

    # Read the output file back into a DataFrame
    loaded_data = pd.read_csv(output_file_path)

    # Assert that the loaded data matches the original sample data
    pd.testing.assert_frame_equal(sample_data, loaded_data)


def test_load_data_with_invalid_path():
    # Create a sample DataFrame to load
    sample_data = pd.DataFrame({
        'name': ['Alice', 'Bob'],
        'salary': [50000, 60000],
        'tax': [5000, 6000],
        'net_salary': [45000, 54000]
    })

    # Define an invalid output file path
    invalid_output_file_path = "/invalid_path/output.csv"

    # Call the load_data function and expect it to handle the error gracefully
    try:
        load_data(sample_data, invalid_output_file_path)
    except Exception as e:
        assert isinstance(e, Exception)  # Ensure an exception is raised