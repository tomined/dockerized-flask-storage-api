# app/Dockerfile

# Use a lightweight Python base image.
# python:3.9-slim-buster is a good choice for Debian-based systems.
# Alternatively, python:3.9-slim is more generic.
FROM python:3.11-slim

# Set the working directory inside the container.
# All subsequent commands will be executed from this directory.
WORKDIR /app

# Copy the requirements.txt file first to leverage Docker's build cache.
# If only requirements.txt changes, this step will be rebuilt, but not subsequent ones.
COPY requirements.txt .

# Install Python dependencies.
# --no-cache-dir ensures pip does not store cache, reducing image size.
# -r requirements.txt installs packages listed in the file.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container.
# This copies everything from the current build context (./app) into /app.
COPY . .

# Create the 'files' directory if it doesn't exist.
# This ensures the directory is present before the application starts.
RUN mkdir -p files

# Declare /app/files as a volume.
# This indicates that the directory is intended to hold external data,
# which can be mounted by the host for persistence (as configured in docker-compose.yml).
VOLUME /app/files

# Expose port 8000.
# This informs Docker that the container listens on this port at runtime.
EXPOSE 8000

# Command to run the application using Gunicorn.
# gunicorn: The WSGI HTTP server.
# --bind 0.0.0.0:8000: Binds Gunicorn to all network interfaces on port 8000.
# app:app: Specifies the Flask application instance (from app.py, where 'app' is the Flask instance name).
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]