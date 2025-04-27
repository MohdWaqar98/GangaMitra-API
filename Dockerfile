# Use a lightweight Python base image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of the project files
COPY . .

# Expose the port (Railway uses PORT env var, so we'll handle it dynamically)
EXPOSE 8080

# Set environment variable for production
ENV FLASK_ENV=production

# Command to run the app
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
