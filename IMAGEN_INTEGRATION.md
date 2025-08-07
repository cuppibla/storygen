# Google Imagen Integration for StoryGen

This document describes the Google Imagen integration that enables AI-generated visuals for story keyframes.

## Overview

The StoryGen application now supports generating realistic images using Google's Imagen API through Vertex AI. When users generate a story, the AI agent automatically creates 4 visual keyframes that represent key moments from the narrative.

## Features

- **Automated Image Generation**: After generating a story, the AI automatically creates 4 visual keyframes
- **Custom ADK Tool**: Uses a custom Agent Development Kit (ADK) tool that wraps the Google Imagen API
- **Real-time Updates**: Images are generated and displayed in real-time via WebSocket
- **Interactive UI**: Users can view full-size images and download them
- **Fallback Graceful**: If Imagen is not configured, the app falls back to placeholder images

## Architecture

### Backend Components

1. **`imagen_tool.py`**: Custom ADK tool that wraps Google Imagen API
   - Handles image generation requests
   - Converts images to base64 for transport
   - Provides error handling and validation

2. **Updated `agent.py`**: Enhanced story agent with image generation capabilities
   - Includes the Imagen tool in its toolset
   - Updated instructions to generate both stories and images
   - Workflow: Story → Identify keyframes → Generate images

3. **Enhanced `main.py`**: WebSocket handling for image data
   - Processes tool call events
   - Handles image generation results
   - Sends image data to frontend

### Frontend Components

1. **Updated `page.tsx`**: Main application with image state management
   - Tracks generated images
   - Displays image generation status
   - Handles WebSocket messages for images

2. **Enhanced `image-keyframes.tsx`**: Interactive image display component
   - Shows generated images or placeholders
   - Provides download and full-view functionality
   - Loading states and progress indicators

## Setup Instructions

### Prerequisites

1. **Google Cloud Project** with Vertex AI API enabled
2. **Service Account** with Vertex AI User role
3. **Service Account JSON Key** downloaded

### Quick Setup

Run the automated setup script:

```bash
./setup-imagen.sh
```

### Manual Setup

1. **Install Dependencies**:
   ```bash
   cd backend
   source .venv/bin/activate
   pip install google-cloud-aiplatform>=1.38.0
   ```

2. **Configure Environment**:
   ```bash
   # Edit backend/.env
   GOOGLE_CLOUD_PROJECT_ID=your_gcp_project_id
   GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json
   ```

3. **Test the Integration**:
   ```bash
   # Start backend
   cd backend && source .venv/bin/activate && uvicorn main:app --reload --host 0.0.0.0 --port 8000
   
   # Start frontend (new terminal)
   npm run dev
   ```

## How It Works

### Story and Image Generation Flow

1. **User Input**: User enters keywords and clicks "Generate Story"
2. **Story Generation**: AI agent generates a creative story based on keywords
3. **Keyframe Identification**: Agent identifies 4 key moments from the story
4. **Image Prompts**: Agent creates detailed prompts for each keyframe
5. **Image Generation**: Imagen tool generates images for each prompt
6. **Real-time Display**: Images are displayed as they're generated

### WebSocket Message Types

- `tool_call`: Notifies when image generation starts
- `image_generated`: Contains generated image data
- `story_chunk`: Story text content (existing)
- `turn_complete`: Indicates completion of story and images

### Image Data Format

Images are returned as base64-encoded data:

```json
{
  "success": true,
  "prompt": "A photorealistic cyberpunk cityscape...",
  "images": [
    {
      "index": 0,
      "base64": "iVBORw0KGgoAAAANSUhEUgAA...",
      "format": "png"
    }
  ]
}
```

## Configuration Options

### Imagen Tool Parameters

- **prompt**: Detailed text description (required)
- **negative_prompt**: What to exclude (optional)
- **aspect_ratio**: Image dimensions ("16:9", "1:1", etc.)
- **number_of_images**: How many to generate (1-4)

### Agent Instructions

The agent is configured to:
- Generate complete stories first
- Create 4 distinct keyframes
- Use cinematic, photorealistic prompts
- Match image style to story tone

## Error Handling

- **Missing Configuration**: App functions normally without Imagen setup
- **API Errors**: Graceful fallback to placeholder images
- **Network Issues**: Status indicators and retry options
- **Invalid Responses**: Error messages in the UI

## Troubleshooting

### Common Issues

1. **"Address already in use" Error**:
   ```bash
   # Find and kill the process using port 8000
   lsof -ti:8000 | xargs kill -9
   ```

2. **Imagen Tool Not Initialized**:
   - Check `GOOGLE_CLOUD_PROJECT_ID` in `.env`
   - Verify service account key path
   - Ensure Vertex AI API is enabled

3. **Images Not Displaying**:
   - Check browser console for errors
   - Verify WebSocket connection
   - Confirm base64 data format

### Debug Mode

Enable detailed logging:

```python
# In backend/main.py
logging.basicConfig(level=logging.DEBUG)
```

## Customization

### Modifying Image Prompts

Edit the agent instructions in `backend/story_agent/agent.py`:

```python
instruction="""...
Guidelines for image generation:
- Use your preferred style (e.g., "anime style", "oil painting")
- Modify aspect ratio preferences
- Adjust negative prompts for consistent style
..."""
```

### Changing Image Count

Modify the frontend to support different numbers of keyframes by updating the grid layout in `image-keyframes.tsx`.

### Adding Image Filters

Extend the Imagen tool to support additional parameters like style filters or image editing operations.

## Performance Considerations

- **Image Generation Time**: 10-30 seconds per image
- **Base64 Size**: ~1-2MB per image in transport
- **Memory Usage**: Images are stored in component state
- **Network**: WebSocket handles large payloads efficiently

## Security Notes

- Service account keys should be secured and not committed to version control
- Consider using Workload Identity for production deployments
- Base64 images are temporary and not persisted server-side
- User-generated prompts are passed to Imagen API

## Future Enhancements

- **Image Persistence**: Save generated images to cloud storage
- **Style Consistency**: Maintain character/style consistency across keyframes
- **User Controls**: Allow users to modify prompts or regenerate specific images
- **Image Editing**: Add basic editing capabilities (crop, filter, etc.)
- **Batch Generation**: Generate multiple image variations per keyframe 