FROM python:3.11-slim

WORKDIR /app

# Install deps + curl + iputils-ping
RUN apt-get update && apt-get install -y curl iputils-ping && rm -rf /var/lib/apt/lists/*

# Install Python deps
RUN pip install --no-cache-dir flask requests

# Copy app code
COPY . /app

EXPOSE 3000

CMD ["python3", "/app/app/server.py"]
