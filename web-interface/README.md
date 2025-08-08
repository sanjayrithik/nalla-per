# HPTA Web Interface

🌐 **Hacking Penetration Testing Assistant** - AI-Powered Security Tool Interface

A modern web interface that uses Gemini AI to convert natural language tasks into CLI commands and provides intelligent summaries of security tool outputs.

## 🚀 Features

### Frontend Features
- ✅ **Gemini API Key Management**: Support for 3-5 API keys with automatic rotation
- ✅ **Key Status Monitoring**: Real-time status display (working/expired)
- ✅ **Auto Key Fallback**: Automatic switching to next working key if one fails
- ✅ **Natural Language Input**: Submit tasks in plain English
- ✅ **Modern UI**: Beautiful, responsive interface with Bootstrap 5
- ✅ **Real-time Results**: Live updates and progress indicators

### Backend Features
- ✅ **AI-Powered Task Conversion**: Uses Gemini to convert tasks → CLI commands
- ✅ **CLI Server Integration**: Communicates with local CLI Docker server
- ✅ **Intelligent Summarization**: AI-powered output analysis and summarization
- ✅ **Key Management**: In-memory key storage with validation and rotation
- ✅ **Error Handling**: Comprehensive error handling and user feedback

## 🏗️ Architecture

```
┌─────────────────┐     POST /api/processCommand     ┌─────────────────┐
│   Web Frontend  │  ─────────────────────────────▶  │  Flask Backend  │
│  (localhost:3000)│                                  │  (Gemini AI)    │
│  - Enter Keys   │                                  │  - Task → CMD   │
│  - Submit Task  │  ◀─────────────────────────────  │  - Summarize    │
│  - View Results │     Summarized Output JSON       │  - Key Rotation │
└─────────────────┘                                  └─────────────────┘
                                                           │
                                                           ▼
                                              POST http://localhost:5000/run
                                                           │
                                              ┌─────────────────┐
                                              │  CLI Docker     │
                                              │  Server         │
                                              │  - Nmap/Tools   │
                                              │  - Raw Output   │
                                              └─────────────────┘
```

## 📦 Installation

### Prerequisites
- Docker and Docker Compose
- Gemini API keys (1-5 keys recommended)

### Quick Start

1. **Clone and Navigate**
   ```bash
   cd web-interface
   ```

2. **Build and Run**
   ```bash
   docker-compose up --build
   ```

3. **Access the Interface**
   - Open your browser to `http://localhost:3000`
   - The CLI server will be available at `http://localhost:5001`

## 🔧 Configuration

### Environment Variables
- `FLASK_ENV`: Set to `production` for production deployment
- `GEMINI_API_KEYS`: Optional environment variable for default keys

### API Key Setup
1. Get Gemini API keys from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Enter 1-5 keys in the web interface
3. Keys are validated automatically
4. Working keys are used for AI operations

## 🎯 Usage

### Step 1: Initialize API Keys
1. Enter your Gemini API keys (1-5 keys)
2. Click "Initialize Keys"
3. Verify key status indicators

### Step 2: Submit Security Tasks
Enter natural language commands like:
- `"scan example.com"`
- `"check for SQL injection on test.com"`
- `"analyze port 80 on localhost"`
- `"perform a quick network scan"`

### Step 3: View Results
The interface displays:
- **Task Summary**: Original request
- **Generated Command**: CLI command created by AI
- **AI Summary**: Intelligent analysis of results
- **Raw Output**: Complete tool output

## 🔌 API Endpoints

### Frontend → Backend
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/initKeys` | POST | Initialize and validate API keys |
| `/api/processCommand` | POST | Process task and return results |
| `/api/keyStatus` | GET | Get current key status |

### Backend → CLI Server
| URL | Method | Payload |
|-----|--------|---------|
| `http://localhost:5001/run` | POST | `{"command": "nmap -v example.com"}` |

## 🛡️ Security Features

### Command Validation
- Whitelist of allowed command prefixes
- Prevents execution of dangerous commands
- Input sanitization and validation

### API Key Security
- Keys stored in memory only
- Automatic key rotation on failures
- Secure key validation process

## 🧪 Testing

### Sample Tasks
```bash
# Network scanning
"scan example.com"
"perform a port scan on localhost"

# Security testing
"check for SQL injection on test.com"
"test for XSS vulnerabilities"

# Analysis
"analyze the network topology"
"check for open ports"
```

### Expected Flow
1. User enters: `"scan example.com"`
2. AI converts to: `"nmap -v example.com"`
3. CLI server executes command
4. AI summarizes results
5. User sees structured output

## 🐛 Troubleshooting

### Common Issues

**Keys not working**
- Verify API keys are valid
- Check internet connectivity
- Ensure keys have sufficient quota

**CLI server connection failed**
- Verify CLI server is running on port 5001
- Check Docker container status
- Review server logs

**Commands not executing**
- Check command whitelist
- Verify tool availability in categories/
- Review error messages

### Logs
```bash
# View web interface logs
docker-compose logs web-interface

# View CLI server logs
docker-compose logs cli-server

# Follow logs in real-time
docker-compose logs -f
```

## 🔄 Development

### Local Development
```bash
# Install dependencies
pip install -r app/requirements.txt

# Run Flask development server
cd app
python server.py

# Run CLI server separately
cd ../server
python main.py
```

### File Structure
```
web-interface/
├── Dockerfile                 # Container configuration
├── docker-compose.yml         # Multi-service setup
├── README.md                  # This file
└── app/
    ├── server.py              # Flask backend
    ├── gemini_handler.py      # AI key management
    ├── requirements.txt       # Python dependencies
    ├── templates/
    │   └── index.html         # Main UI template
    └── static/
        └── script.js          # Frontend JavaScript
```

## 📝 License

This project is part of the HPTA (Hacking Penetration Testing Assistant) suite.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For issues and questions:
- Check the troubleshooting section
- Review the logs
- Open an issue on GitHub 