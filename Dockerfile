# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables to avoid Python writing pyc files
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt into the container at /app
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Expose port 8000 for the Django app
EXPOSE 8000

# Run the Django application (make sure it's using the appropriate settings)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
