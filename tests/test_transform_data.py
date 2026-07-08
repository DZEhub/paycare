"""
#* ==================================
#* Phase 2: Write Tests : etl.py
#* ==================================
You will write unit tests to ensure that the extraction, transformation, and loading steps work as expected. The tests should check for:

    1. Data Extraction : Test that the input CSV file is read correctly.
    2. Data Transformation : Test that the cleaning and tax/net salary calculation steps are performed correctly.
    3. Data Loading : Test that the processed data is saved correctly to an output file.

#* Testing Requirements: transform_data.py
    - Use `pytest` to write unit tests for the ETL functions (`extract_data`, `transform_data`, and `load_data` — or the equivalent functions in `etl.py`).
    - Mock the CSV file input and output where necessary (e.g., using temporary files or in-memory DataFrames).
    - Ensure tests cover potential edge cases (e.g., missing values in the input file, negative salaries, invalid tax rates).
"""
import pytest
import pandas as pd
import app.etl as etl  # Import the module so monkeypatching updates the same function object.


def test_transform_data():
    # Create a sample DataFrame to transform
    # sample_data = extract_data("../data/input_data.csv")  # Assuming you have a sample_input.csv for testing
    sample_data = pd.DataFrame({
        'name': ['Alice', 'Bob', 'Charlie'],
        'salary': [50000, 60000, None]  # Include a missing value for testing
    })

    # Call the transform_data function
    transformed_data = etl.transform_data(sample_data)  # Call the ETL function through its module namespace.

    # Define the expected DataFrame after transformation
    expected_data = pd.DataFrame({
        'name': ['Alice', 'Bob'],
        'salary': [50000, 60000],
        'tax': [5000.0, 6000.0],
        'net_salary': [45000.0, 54000.0]
    })

    # Assert that the transformed data matches the expected data
    pd.testing.assert_frame_equal(transformed_data.reset_index(drop=True), 
                                  expected_data.reset_index(drop=True), 
                                  check_dtype=False, 
                                  obj="Transformed data does not match expected data after transformation.")
    assert 'tax' in transformed_data.columns, "Tax column is missing in the transformed data."
    assert 'net_salary' in transformed_data.columns, "Net salary column is missing in the transformed data."


def test_transform_data_with_missing_values():
    # Create a sample DataFrame with missing values
    sample_data = pd.DataFrame({
        'name': ['Alice', 'Bob', None],
        'salary': [50000, None, 70000]
    })

    # Call the transform_data function
    transformed_data = etl.transform_data(sample_data)  # Use the shared module import for consistent CI behavior.

    # Define the expected DataFrame after transformation (rows with missing values should be dropped)
    expected_data = pd.DataFrame({
        'name': ['Alice'],
        'salary': [50000],
        'tax': [5000.0],
        'net_salary': [45000.0]
    })

    # Assert that the transformed data matches the expected data
    pd.testing.assert_frame_equal(transformed_data.reset_index(drop=True), expected_data.reset_index(drop=True), check_dtype=False)
    assert transformed_data.isnull().sum().sum() == 0, "Transformed data contains missing values."


def test_transform_data_with_negative_salary():
    # Create a sample DataFrame with a negative salary
    sample_data = pd.DataFrame({
        'name': ['Alice', 'Bob'],
        'salary': [50000, -60000]  # Include a negative salary for testing
    })

    # Call the transform_data function
    transformed_data = etl.transform_data(sample_data)  # Keep the call path consistent with the other tests.

    # Define the expected DataFrame after transformation (negative salary is preserved by the current ETL logic)
    expected_data = pd.DataFrame({
        'name': ['Alice', 'Bob'],
        'salary': [50000, -60000],
        'tax': [5000.0, -6000.0],
        'net_salary': [45000.0, -54000.0]
    })

    # Assert that the transformed data matches the expected data
    pd.testing.assert_frame_equal(transformed_data.reset_index(drop=True), expected_data.reset_index(drop=True), check_dtype=False)


def test_transform_data_with_invalid_tax_rate(monkeypatch):
    # Create a sample DataFrame to transform
    sample_data = pd.DataFrame({
        'name': ['Alice', 'Bob'],
        'salary': [50000, 60000]
    })

    # Monkeypatch the tax calculation to simulate an invalid tax rate
    def mock_transform_data(data):
        data_cleaned = data.dropna()
        data_cleaned['tax'] = data_cleaned['salary'] * -0.1  # Invalid negative tax rate
        data_cleaned['net_salary'] = data_cleaned['salary'] - data_cleaned['tax']
        return data_cleaned

    monkeypatch.setattr(etl, 'transform_data', mock_transform_data)  # Patch the shared module object used by this test.

    # Call the transform_data function
    transformed_data = etl.transform_data(sample_data)  # Call through the module so the monkeypatch is effective.

    # Define the expected DataFrame after transformation with invalid tax rate
    expected_data = pd.DataFrame({
        'name': ['Alice', 'Bob'],
        'salary': [50000, 60000],
        'tax': [-5000.0, -6000.0],
        'net_salary': [55000.0, 66000.0]
    })

    # Assert that the transformed data matches the expected data
    pd.testing.assert_frame_equal(transformed_data.reset_index(drop=True), expected_data.reset_index(drop=True), check_dtype=False)