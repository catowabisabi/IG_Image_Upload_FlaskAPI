# Use an official Python runtime as a parent image
FROM python:3.10
# Set the working directory in the container
WORKDIR /app

# Install system dependencies needed for Pillow and other packages
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libopenjp2-7-dev \
    libtiff5-dev \
    tk-dev \
    tcl-dev \
    libharfbuzz-dev \
    libfribidi-dev \
    libxcb1-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Upgrade pip and install wheel first
RUN pip install --upgrade pip setuptools wheel

# Install Pillow first with explicit dependencies
RUN pip install --no-cache-dir pillow>=8.1.1

# Install remaining packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . .

# Create uploads and sessions directories and set permissions
RUN mkdir -p /app/uploads /app/sessions && chmod 777 /app/uploads /app/sessions

# Make port 5005 available to the world outside this container
EXPOSE 5005

# Run the command to start the server
CMD ["python", "instagram_api_flask.py"] 