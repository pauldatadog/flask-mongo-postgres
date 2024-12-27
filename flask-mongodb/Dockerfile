# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install ddtrace

ENV DD_SERVCE online-retail
ENV DD_ENV development
ENV DD_VERSION 1.0.0

# Expose the Flask app's port
EXPOSE 5000

# Run the application
CMD ["ddtrace-run", "python3", "app.py"]
