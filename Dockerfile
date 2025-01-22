# Use an official Python image as the base
FROM python:3.13.1-slim-bullseye

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the container
COPY . .

# Expose the FastAPI default port
EXPOSE 8000

# Set the environment variable for Hugging Face token
ENV HF_HOME=/root/.cache/huggingface

# Run the FastAPI application using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
