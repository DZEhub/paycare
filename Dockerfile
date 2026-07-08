# Phase 1: Write the Dockerfile
# You need to containerize the Python ETL application using Docker. 
# The Dockerfile will allow anyone in the company to run the ETL pipeline locally or in a production environment with the necessary dependencies packaged in a container.
#
# The Docker container will:
#   - Install necessary dependencies (e.g., Pandas).
#   - Run the ETL script (etl.py) that reads input data from a CSV file, processes it, and saves the output.

# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt && \
pip cache purge

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Run etl.py when the container launches
CMD ["python", "etl.py"]