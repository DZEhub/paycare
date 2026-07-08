"""
#* ==================================
#* Phase 2: Write Tests : etl.py
#* ==================================
You will write unit tests to ensure that the extraction, transformation, and loading steps work as expected. The tests should check for:

    1. Data Extraction : Test that the input CSV file is read correctly.
    2. Data Transformation : Test that the cleaning and tax/net salary calculation steps are performed correctly.
    3. Data Loading : Test that the processed data is saved correctly to an output file.

#* Testing Requirements: test_extract_data.py
    - Use `pytest` to write unit tests for the ETL functions (`extract_data`, `transform_data`, and `load_data` — or the equivalent functions in `etl.py`).
    - Mock the CSV file input and output where necessary (e.g., using temporary files or in-memory DataFrames).
    - Ensure tests cover potential edge cases (e.g., missing values in the input file, negative salaries, invalid tax rates).
"""
import pytest
import pandas as pd
from app.etl import extract_data

def test_extract_data(tmp_path):
    # Create a sample CSV file in the temporary directory
    sample_csv = tmp_path / "sample.csv"
    sample_data = pd.DataFrame({
        'name': ['Alice', 'Bob'],
        'salary': [50000, 60000]
    })
    sample_data.to_csv(sample_csv, index=False)

    # Call the extract_data function
    extracted_data = extract_data(sample_csv)

    # Assert that the extracted data matches the original sample data
    pd.testing.assert_frame_equal(extracted_data, sample_data)


def test_extract_data_with_invalid_path():
    # Define an invalid file path
    invalid_file_path = "/invalid_path/sample.csv"

    # Call the extract_data function and expect it to handle the error gracefully
    extracted_data = extract_data(invalid_file_path)

    # Assert that the extracted data is None due to the invalid path
    assert extracted_data is None


def test_extract_data_with_empty_file(tmp_path):
    # Create an empty CSV file in the temporary directory
    empty_csv = tmp_path / "empty.csv"
    empty_csv.write_text("")

    # Call the extract_data function
    extracted_data = extract_data(empty_csv)

    # Assert that the extracted data is None due to the empty file
    assert extracted_data is None


def test_extract_data_with_missing_values(tmp_path):
    # Create a sample CSV file with missing values in the temporary directory
    sample_csv = tmp_path / "sample_with_missing.csv"
    sample_data = pd.DataFrame({
        'name': ['Alice', None, 'Charlie'],
        'salary': [50000, 60000, None]
    })
    sample_data.to_csv(sample_csv, index=False)

    # Call the extract_data function
    extracted_data = extract_data(sample_csv)

    # Assert that the extracted data matches the original sample data
    pd.testing.assert_frame_equal(extracted_data, sample_data) 


def test_extract_data_with_invalid_format(tmp_path):
    # # Create a sample CSV file with invalid format in the temporary directory
    # sample_csv = tmp_path / "sample_invalid_format.csv"
    # sample_csv.write_text("name,salary\nAlice,50000\nBob,60000\nCharlie,invalid_salary")

    # # Call the extract_data function
    # extracted_data = extract_data(sample_csv)

    # # Assert that the extracted data is None due to the invalid format
    # assert extracted_data is None
    pass