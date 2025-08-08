@echo off
echo 🚀 Starting HPTA Web Interface...

REM Check if Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not running. Please start Docker first.
    pause
    exit /b 1
)

REM Check if docker-compose is available
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ docker-compose is not installed. Please install it first.
    pause
    exit /b 1
)

REM Build and start the services
echo 📦 Building and starting services...
docker-compose up --build -d

REM Wait for services to be ready
echo ⏳ Waiting for services to start...
timeout /t 10 /nobreak >nul

REM Check service status
echo 🔍 Checking service status...
docker-compose ps

REM Show access information
echo.
echo ✅ HPTA Web Interface is ready!
echo.
echo 🌐 Web Interface: http://localhost:3000
echo 🔧 CLI Server: http://localhost:5000
echo.
echo 📋 Next steps:
echo 1. Open http://localhost:3000 in your browser
echo 2. Enter your Gemini API keys
echo 3. Start using the interface!
echo.
echo 📊 View logs: docker-compose logs -f
echo 🛑 Stop services: docker-compose down
echo.
pause 