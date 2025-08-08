# 🚀 HPTA Web Interface - Quick Start

## ⚡ Get Started in 3 Steps

### 1. Start the System
**Windows:**
```cmd
cd web-interface
start.bat
```

**Linux/Mac:**
```bash
cd web-interface
./start.sh
```

**Manual:**
```bash
cd web-interface
docker-compose up --build -d
```

### 2. Access the Interface
Open your browser and go to: **http://localhost:3000**

**Services:**
- Web Interface: http://localhost:3000
- CLI Server: http://localhost:5001

### 3. Initialize API Keys
1. Get Gemini API keys from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Enter 1-5 keys in the web interface
3. Click "Initialize Keys"
4. Verify key status indicators

## 🎯 Try It Out

Enter a security task like:
- `"scan example.com"`
- `"check for SQL injection on test.com"`
- `"analyze port 80 on localhost"`

## 📊 What You'll See

1. **Task Summary**: Your original request
2. **Generated Command**: CLI command created by AI
3. **AI Summary**: Intelligent analysis of results
4. **Raw Output**: Complete tool output

## 🛠️ Troubleshooting

**Services not starting?**
```bash
docker-compose logs
```

**Test the setup:**
```bash
python test_setup.py
```

**Stop services:**
```bash
docker-compose down
```

## 📁 File Structure
```
web-interface/
├── start.bat              # Windows startup
├── start.sh               # Linux/Mac startup
├── docker-compose.yml     # Multi-service setup
├── Dockerfile             # Container config
├── test_setup.py          # Setup verification
├── README.md              # Full documentation
└── app/
    ├── server.py          # Flask backend
    ├── gemini_handler.py  # AI management
    ├── templates/
    │   └── index.html     # Web UI
    └── static/
        └── script.js      # Frontend logic
```

## 🔗 Useful Commands

```bash
# View logs
docker-compose logs -f

# Restart services
docker-compose restart

# Rebuild and start
docker-compose up --build

# Stop everything
docker-compose down
```

## 🆘 Need Help?

- Check the full [README.md](README.md) for detailed documentation
- Review logs: `docker-compose logs`
- Test setup: `python test_setup.py`
- Ensure Docker is running
- Verify Gemini API keys are valid

---

**Happy Hacking! 🛡️** 