# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install ddtrace

# Copy the database setup script
COPY postgres_setup.sql /docker-entrypoint-initdb.d/

# Expose the application's port
EXPOSE 5000

# Command to run the application
CMD ["ddtrace-run", "python3", "app.py"]
