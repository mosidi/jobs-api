# # Use an official Python runtime as a parent image
# FROM python:3.8-slim as Job-posting-api

# # Set the working directory in the container
# WORKDIR /app

# # Update package lists and install necessary packages
# RUN apt-get update && \
#     apt-get install -y python3-pip && \
#     pip3 install --upgrade pip

# # Install awscli using pip
# RUN pip3 install awscli

# # Copy the current directory contents into the container at /app
# COPY . /app

# # Install any needed packages specified in requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt
# # Make port 80 available to the world outside this container
# EXPOSE 80
# # Run app.py when the container launches
# CMD ["uvicorn", "main:app",, "0.0.0.0", "--port", "80"] #
# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME JobPostingFastAPI

# Run main.py when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
