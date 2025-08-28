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

# Expose the port the app runs on
EXPOSE 5000

# Run the app using Gunicorn with SocketIO support
CMD ["gunicorn", "--worker-class", "eventlet", "-w", "1", "--bind", "0.0.0.0:5000", "wsgi:socketio"]
