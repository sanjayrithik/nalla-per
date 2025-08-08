# CLI Server Dockerfile - Apt-only Flask Install (No PyPI)
FROM kalilinux/kali-rolling

ENV DEBIAN_FRONTEND=noninteractive

# Update and install all dependencies, including Flask from apt
RUN apt-get update -y --fix-missing && \
    apt-get install -y --no-install-recommends \
    nmap \
    sqlmap \
    curl \
    wget \
    whois \
    net-tools \
    python3 \
    python3-pip \
    python3-setuptools \
    python3-wheel \
    python3-venv \
    build-essential \
    ca-certificates \
    python3-flask \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY server /app/server
COPY categories /app/categories

EXPOSE 5000

CMD ["python3", "/app/server/main.py"]
