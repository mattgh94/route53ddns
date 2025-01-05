# Use the official Python base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the requirements file into the container
COPY requirements.txt ./
COPY .aws /root/.aws

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the script into the container
COPY awsddns.py .

# Run the Python script
CMD ["python", "./awsddns.py"]