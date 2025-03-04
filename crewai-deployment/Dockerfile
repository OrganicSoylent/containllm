FROM python:3.12

# Set the working directory in the container
WORKDIR /app
RUN mkdir marketing_crew/ \
    && mkdir stock_analysis/ \
    && mkdir trip_planner/

# Copy the application code
COPY crewai_setup/crews/marketing_strategy/ /app/marketing_crew/
COPY crewai_setup/crews/stock_analysis/ /app/stock_analysis/
COPY crewai_setup/crews/trip_planner/ /app/trip_planner/

# Ensure execute permissions for your scripts
RUN chmod +x /app/marketing_crew/ \
    && chmod +x /app/stock_analysis/ \
    && chmod +x /app/trip_planner/

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Expose port if required (modify as needed)
EXPOSE 8080

# Run the container indefinitely
CMD ["bash", "-c", "echo 'Container running' && tail -f /dev/null"]