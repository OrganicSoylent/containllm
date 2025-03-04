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

# Log the file structure to ensure the directories and files are copied correctly
RUN echo "Listing /app/ directory contents:" \
    && ls -l /app/ \
    && echo "Listing marketing_crew directory contents:" \
    && ls -l /app/marketing_crew/ \
    && echo "Listing stock_analysis directory contents:" \
    && ls -l /app/stock_analysis/ \
    && echo "Listing trip_planner directory contents:" \
    && ls -l /app/trip_planner/

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Expose port if required (modify as needed)
EXPOSE 8080

# Log environment info to help debugging
RUN echo "Environment variables:" \
    && printenv \
    && echo "Python version:" \
    && python --version

# Run the container indefinitely
CMD ["bash", "-c", "echo 'Container running' && tail -f /dev/null"]