# Use the official Python image as the base image
FROM python:3.8-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required Python packages
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY run.py .
COPY app ./app

# Define the command to run the Flask app
CMD ["gunicorn", "run:app", "--bind=0.0.0.0:5003", "--log-level=DEBUG", "--workers=2"]
