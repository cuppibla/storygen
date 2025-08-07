# StoryGen - AI-Powered Story Generator

A modern web application that generates creative stories with AI-generated visuals using Google's Agent Development Kit (ADK), Gemini AI models, and Google Imagen for image generation.

[![Built with v0](https://img.shields.io/badge/Built%20with-v0.dev-black?style=for-the-badge)](https://v0.dev/chat/projects/dUF1k4r28Nj)

## ✨ Features

- **AI-Powered Story Generation**: Uses Google's ADK with Gemini models for creative storytelling
- **🎨 AI-Generated Visuals**: Automatically creates 4 visual keyframes using Google Imagen
- **Real-time WebSocket Communication**: Stories and images stream in real-time as they're generated
- **Voice Input Support**: Speak your keywords using browser speech recognition
- **Interactive Image Gallery**: View, download, and explore generated images
- **Modern UI**: Beautiful, responsive design with dark/light mode support
- **Connection Status**: Real-time connection monitoring and error handling
- **Keyword-Based Generation**: Input keywords to influence story themes and visual content

## 🏗️ Architecture

```
Frontend (Next.js)     Backend (FastAPI + ADK)     Google AI
     │                         │                      │
     ├─ React Components       ├─ WebSocket Server    ├─ Gemini Models
     ├─ WebSocket Client       ├─ ADK Integration     ├─ Story Generation
     ├─ Real-time UI           ├─ Session Management  └─ Live API
     └─ Voice Recognition      └─ Error Handling
```

## 🚀 Quick Setup

### Automated Setup (Recommended)

1. **Run the setup script:**
   ```bash
   ./setup-backend.sh
   ```

2. **Configure your Google API key:**
   - Go to [Google AI Studio](https://aistudio.google.com/)
   - Get your API key
   - Edit `backend/.env` and add your key

3. **Start the backend:**
   ```bash
   cd backend
   source .venv/bin/activate
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

4. **Start the frontend:**
   ```bash
   npm run dev
   ```

5. **Open your browser:**
   Visit http://localhost:3000

## 🎨 Google Imagen Integration (Optional)

StoryGen now supports AI-generated visuals using Google Imagen! When enabled, the app automatically creates 4 visual keyframes for each generated story.

### Quick Setup for Imagen

```bash
# Run the automated Imagen setup
./setup-imagen.sh
```

### Manual Imagen Setup

1. **Enable Vertex AI API** in your Google Cloud Console
2. **Create a service account** with Vertex AI User role
3. **Download the service account JSON key**
4. **Configure environment variables** in `backend/.env`:
   ```env
   GOOGLE_CLOUD_PROJECT_ID=your_gcp_project_id
   GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json
   ```

For detailed instructions, see [IMAGEN_INTEGRATION.md](./IMAGEN_INTEGRATION.md)

### Manual Setup

#### Backend Setup

1. **Install Python dependencies:**
   ```bash
   cd backend
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Set SSL certificate:**
   ```bash
   export SSL_CERT_FILE=$(python -m certifi)
   ```

3. **Configure environment:**
   ```bash
   cp env.example .env
   # Edit .env and add your Google API key
   ```

4. **Start the server:**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

#### Frontend Setup

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Start development server:**
   ```bash
   npm run dev
   ```

## 🔧 Configuration

### Google AI Studio API Key

1. Visit [Google AI Studio](https://aistudio.google.com/)
2. Click "Get API key"
3. Create or select a project
4. Generate and copy your API key
5. Add it to `backend/.env`:
   ```env
   GOOGLE_API_KEY=your_actual_api_key_here
   ```

### Environment Variables

**Backend (`backend/.env`):**
```env
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=your_actual_google_api_key_here
```

## 🎯 Usage

1. **Enter Keywords**: Type story themes, characters, or settings
2. **Voice Input**: Click the microphone to speak your keywords
3. **Generate Story**: Click "Generate Story" or press Enter
4. **Watch Real-time Generation**: Stories appear as they're being created
5. **Connection Status**: Monitor your connection to the AI service

### Example Keywords
- "robot detective mystery"
- "space adventure friendship"
- "magical forest dragon"
- "cyberpunk hacker AI"

## 🛠️ Development

### Project Structure

```
storygen-1/
├── frontend/
│   ├── app/                    # Next.js app directory
│   ├── components/             # React components
│   └── ...                     # Frontend files
├── backend/                    # Python ADK backend
│   ├── main.py                # FastAPI server
│   ├── story_agent/           # ADK agent definition
│   ├── requirements.txt       # Python dependencies
│   └── README.md              # Backend documentation
├── setup-backend.sh           # Automated setup script
└── README.md                  # This file
```

### API Endpoints

**WebSocket**: `ws://localhost:8000/ws/{user_id}`
- Real-time story generation
- Bidirectional communication
- Session management

**HTTP**:
- `GET /`: API information
- `GET /health`: Health check

### Message Format

**Client → Server:**
```json
{
  "type": "generate_story",
  "data": "your keywords here"
}
```

**Server → Client:**
```json
{
  "type": "story_chunk",
  "data": "partial story text",
  "partial": true
}
```

## 🔍 Troubleshooting

### Common Issues

1. **"Failed to connect to story generation service"**
   - Ensure backend is running on port 8000
   - Check your Google API key configuration
   - Verify SSL certificate is set: `export SSL_CERT_FILE=$(python -m certifi)`

2. **"API Key Error"**
   - Confirm your API key is valid and active
   - Check the `.env` file format and key placement

3. **WebSocket Connection Issues**
   - Ensure both frontend (3000) and backend (8000) are running
   - Check browser console for detailed error messages

4. **Model Not Available**
   - Try changing to `gemini-2.0-flash-live-001` in `backend/story_agent/agent.py`

### Debug Mode

Enable detailed logging in the backend:
```bash
# Backend logs show connection status and message flow
cd backend
source .venv/bin/activate
uvicorn main:app --reload --log-level debug
```

## 🚀 Production Deployment

For production deployment, consider:

1. **Security**: Add authentication and rate limiting
2. **Scalability**: Use multiple backend instances with load balancing
3. **Session Storage**: Replace in-memory sessions with persistent storage
4. **SSL/TLS**: Use HTTPS/WSS connections
5. **Monitoring**: Add comprehensive logging and health checks

## 📝 License

This project was created with [v0.dev](https://v0.dev) and enhanced with Google ADK integration.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

**Need help?** Check the [backend documentation](backend/README.md) for detailed technical information.