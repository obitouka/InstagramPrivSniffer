# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
# We need to install tkinter for the GUI
RUN apt-get update && apt-get install -y tk
RUN pip install --no-cache-dir -r requirements.txt

# Copy the src directory into the container at /app
COPY src/ ./src/

# Set environment variable for DISPLAY
# This will need to be configured on the host machine
ENV DISPLAY=:0

# Run gui.py when the container launches
CMD ["python", "src/gui.py"]
