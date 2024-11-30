# Base image
FROM python:3.9-slim

# Install curl and other utilities
RUN apt-get update && apt-get install -y curl && apt-get clean

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install dependencies
RUN pip install flask pandas statsmodels matplotlib

# Expose port 5000
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
