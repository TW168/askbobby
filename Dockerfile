# Use a smaller base image
FROM python:3.9.18-alpine

# Expose port 8080
EXPOSE 8080

# Install git
RUN apk add --no-cache git

# Copy Requirements.txt file into app directory
COPY requirements.txt app/requirements.txt

# Install all requirements in requirements.txt
RUN pip install --no-cache-dir -r app/requirements.txt

# Copy all files in current directory into app directory
COPY . /app

# Change Working Directory to app directory
WORKDIR /app

# Run the application
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
