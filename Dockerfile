# syntax=docker/dockerfile:1

# Use an official Python image as a base
FROM python:3.12.5-bookworm

# Set the working directory to /contrans2024
WORKDIR /legiscan_api

# Copy the requirements file into the working directory
COPY requirements.txt requirements.txt

# Install the dependencies using pip
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expose the port for Jupyter Lab
EXPOSE 8888

# Run Jupyter Lab when the container launches
CMD ["jupyter", "lab", "--allow-root", "--ip=0.0.0.0", "--port=8888"]