# Use the official Python base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install Node.js and npm
RUN apt-get update && \
    apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_14.x | bash - && \
    apt-get install -y nodejs && \
    apt-get clean


# Install the Prisma CLI
RUN npm install -g prisma

# Copy the schema.prisma file into the container
COPY prisma /app/prisma

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]


# Run the command to start your application
CMD ["python","-u", "/src/main.py"]
