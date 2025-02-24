# Use an official Python runtime as a parent image
FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY crewai_setup/crews/marketing_strategy/ /app/marketing_crew/
COPY crewai_setup/crews/stock_analysis/ /app/stock_analysis/
COPY crewai_setup/crews/trip_planner/ /app/trip_planner/


# Expose port if required (modify as needed)
EXPOSE 8080

# Run the app -- No run on startup needed
# CMD ["python", "main.py"]