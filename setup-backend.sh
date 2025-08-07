#!/bin/bash

# StoryGen Backend Setup Script
echo "🚀 Setting up StoryGen Backend with ADK..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed. Please install Python 3.8+ first."
    exit 1
fi

# Navigate to backend directory
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Set SSL certificate environment variable
echo "🔒 Setting SSL certificate path..."
export SSL_CERT_FILE=$(python -m certifi)
echo "export SSL_CERT_FILE=\$(python -m certifi)" >> .venv/bin/activate

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚙️ Creating .env file from template..."
    cp env.example .env
    echo ""
    echo "🔑 IMPORTANT: You need to configure your Google API key!"
    echo "   1. Go to https://aistudio.google.com/"
    echo "   2. Click 'Get API key'"
    echo "   3. Create a new project or select an existing one"
    echo "   4. Generate and copy your API key"
    echo "   5. Edit backend/.env and replace 'your_actual_google_api_key_here' with your actual API key"
    echo ""
else
    echo "✅ .env file already exists"
fi

echo ""
echo "🎉 Backend setup complete!"
echo ""
echo "Next steps:"
echo "1. Configure your Google API key in backend/.env"
echo "2. Start the backend server:"
echo "   cd backend"
echo "   source .venv/bin/activate"
echo "   uvicorn main:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "3. In another terminal, start the frontend:"
echo "   npm run dev"
echo ""
echo "4. Open http://localhost:3000 and start generating stories!" 