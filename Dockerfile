FROM python:3.10-slim

# System packages
RUN apt-get update && apt-get install -y gcc libffi-dev build-essential

# Work directory
WORKDIR /app

# Copy project
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8080

# Run the app
CMD ["python", "app.py"]
