<#
## **Paycare 💸180 min**

![](https://lead-program-assets.s3.eu-west-3.amazonaws.com/paycare-logo.png)

You’ve been hired as a **DevOps Engineer** at  **PayCare** , a mid-sized payroll processing company that handles salary and tax calculations for multiple clients. PayCare processes monthly payroll data submitted by clients in CSV format. The company uses an ETL (Extract, Transform, Load) pipeline to clean the raw data, calculate tax and net salaries, and output a clean payroll report.

To ensure reliable and automated payroll processing, PayCare is transitioning to a more automated system using **Docker** for containerization and **GitHub Actions** for continuous integration (CI). Your task is to automate this process and ensure the system is tested and deployable in an automated CI pipeline.

## Your Tasks

PayCare’s payroll data pipeline currently consists of three stages:

1. **Extract** : Read raw payroll data from a CSV file.
2. **Transform** : Clean the data by removing invalid entries and adding tax and net salary columns.
3. **Load** : Save the cleaned and processed data into a new CSV file.

The provided script automates these steps, but the system needs to be further developed into a **containerized application** with automated testing and a  **GitHub Actions CI workflow** . You will need to:

1. **Write a Dockerfile** to containerize the ETL pipeline and run it locally.
2. **Write unit tests** for each step of the ETL pipeline (e.g., data extraction, transformation, loading).
3. **Create a GitHub Actions workflow** that automates testing, building, and running the application in Docker.

## **Scenario**

You are provided with an initial Python script that handles the ETL process for payroll data. The company requires you to extend this by:

1. **Writing a Dockerfile** to containerize the application.
2. **Writing tests** to ensure the code works as expected.
3. **Building a GitHub Actions workflow** to automate testing, building the Docker image, and running the containerized application.

## **Phase 1: Write the Dockerfile**

You need to containerize the Python ETL application using Docker. The Dockerfile will allow anyone in the company to run the ETL pipeline locally or in a production environment with the necessary dependencies packaged in a container.

The Docker container will:
    - Install necessary dependencies (e.g., Pandas).
    - Run the ETL script (`etl.py`) that reads input data from a CSV file, processes it, and saves the output.

### **Dockerfile Requirements**

1. Base the Docker image on an official Python image (e.g., `python:3.9`).
2. Install dependencies (e.g., `pandas`, plus anything listed in `requirements.txt`).
3. Copy the ETL code into the image and set an appropriate working directory.
4. Ensure that the Docker container can be run with mounted volumes for both the input and output CSV files (so that the pipeline can read and write files on the host).
#>

cd .\M04L_MLOps\02_GitHub_Actions\02_TD\
git clone https://github.com/DZEhub/paycare.git
cd paycare

mkdir -p .github/workflows
New-Item -Path ".github/workflows/ci.yml" -ItemType "File" -Force
New-Item -Path "Dockerfile" -ItemType "File" -Force
New-Item -Path "requirements.txt" -ItemType "File" -Force

# add, commit and push the new file to your repository
git status && git add . && git commit -m "update ci.yml for 5th commit" && git push

<#
## **Phase 2: Write Tests**
You will write unit tests to ensure that the extraction, transformation, and loading steps work as expected. The tests should check for:

    1. **Data Extraction** : Test that the input CSV file is read correctly.
    2. **Data Transformation** : Test that the cleaning and tax/net salary calculation steps are performed correctly.
    3. **Data Loading** : Test that the processed data is saved correctly to an output file.

### **Testing Requirements**

    * Use `pytest` to write unit tests for the ETL functions (`extract_data`, `transform_data`, and `load_data` — or the equivalent functions in `etl.py`).
    * Mock the CSV file input and output where necessary (e.g., using temporary files or in-memory DataFrames).
    * Ensure tests cover potential edge cases (e.g., missing values in the input file, negative salaries, invalid tax rates).
#>
mkdir -p tests
New-Item -Path "tests/test_extract_data.py" -ItemType "File" -Force
New-Item -Path "tests/test_transform_data.py" -ItemType "File" -Force
New-Item -Path "tests/test_load_data.py" -ItemType "File" -Force
New-Item -Path "tests/test_etl_process.py" -ItemType "File" -Force

# add, commit and push the new file to your repository
git status && git add . && git commit -m "paycare: update ci.yml and pytest - 1rst commit" && git push