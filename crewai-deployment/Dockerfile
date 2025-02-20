# Use an official Python runtime as a parent image
FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY crew_setup/src/stock_crew /app

# Expose port if required (modify as needed)
EXPOSE 8080

# Define the command to run the application
CMD ["python", "main.py"]