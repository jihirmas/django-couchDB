# Use the latest official Python runtime as a parent image
FROM python:latest

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project directory into the container
COPY . /app/

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variables to prevent Python from writing pyc files to disk and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Run generate_data.py, apply database migrations, and then start the Django server
CMD ["sh", "-c", "python generate_data.py && python manage.py runserver 0.0.0.0:8000"]
