#!/bin/bash

echo "🎨 Setting up Google Imagen integration for StoryGen..."

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Backend setup
echo "📦 Installing backend dependencies..."
cd backend

# Install new Python dependencies
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
    pip install google-cloud-aiplatform>=1.38.0
    echo "✅ Backend dependencies installed"
else
    echo "⚠️  Virtual environment not found. Please run setup-backend.sh first"
    exit 1
fi

cd ..

echo "🔧 Setting up Google Cloud configuration..."

# Check if .env file exists
if [ ! -f "backend/.env" ]; then
    echo "📄 Creating .env file from template..."
    cp backend/env.example backend/.env
    echo "⚠️  Please edit backend/.env and add your Google Cloud configuration:"
    echo "   - GOOGLE_CLOUD_PROJECT_ID=your_gcp_project_id"
    echo "   - GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json"
else
    echo "📄 .env file already exists"
fi

echo ""
echo "🌟 Google Imagen integration setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Set up Google Cloud Project:"
echo "   - Go to https://console.cloud.google.com/"
echo "   - Create a new project or select existing one"
echo "   - Enable the Vertex AI API"
echo "   - Create a service account with Vertex AI User role"
echo "   - Download the service account JSON key"
echo ""
echo "2. Update backend/.env file:"
echo "   - Set GOOGLE_CLOUD_PROJECT_ID to your project ID"
echo "   - Set GOOGLE_APPLICATION_CREDENTIALS to your service account key path"
echo ""
echo "3. Test the integration:"
echo "   - Start the backend: cd backend && source .venv/bin/activate && uvicorn main:app --reload --host 0.0.0.0 --port 8000"
echo "   - Start the frontend: npm run dev"
echo "   - Generate a story with keywords and watch as images are created!"
echo ""
echo "🎉 Your StoryGen app now supports AI-generated visuals!" 