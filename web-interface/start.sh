#!/bin/bash

# HPTA Web Interface Startup Script
echo "🚀 Starting HPTA Web Interface..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose is not installed. Please install it first."
    exit 1
fi

# Build and start the services
echo "📦 Building and starting services..."
docker-compose up --build -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 10

# Check service status
echo "🔍 Checking service status..."
docker-compose ps

# Show access information
echo ""
echo "✅ HPTA Web Interface is ready!"
echo ""
echo "🌐 Web Interface: http://localhost:3000"
echo "🔧 CLI Server: http://localhost:5000"
echo ""
echo "📋 Next steps:"
echo "1. Open http://localhost:3000 in your browser"
echo "2. Enter your Gemini API keys"
echo "3. Start using the interface!"
echo ""
echo "📊 View logs: docker-compose logs -f"
echo "🛑 Stop services: docker-compose down"
echo "" 