import os
import json
import asyncio
import logging
from pathlib import Path
from dotenv import load_dotenv

from google.genai.types import Content, Part
from google.adk.runners import InMemoryRunner
from google.adk.sessions.in_memory_session_service import InMemorySessionService

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from story_agent.workflow_agent import create_story_workflow_agent

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Application constants
APP_NAME = "storygen_app"

# Initialize FastAPI app
app = FastAPI(title="StoryGen Backend", description="ADK-powered story generation backend")

# Add CORS middleware to allow frontend connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Next.js default ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize session service and workflow agent
session_service = InMemorySessionService()
workflow_agent = create_story_workflow_agent()

async def run_story_workflow(user_id: str, keywords: str):
    """
    Run the story generation workflow for the given keywords
    
    Args:
        user_id: Unique identifier for the user session
        keywords: Keywords to generate story from
        
    Returns:
        The workflow result
    """
    try:
        # Create a Runner with the workflow agent
        runner = InMemoryRunner(
            app_name=APP_NAME,
            agent=workflow_agent,
        )

        # Create a Session
        session = await runner.session_service.create_session(
            app_name=APP_NAME,
            user_id=user_id,
        )

        # Create content for the workflow
        content = Content(
            role="user", 
            parts=[Part.from_text(text=f"Generate a creative short story based on these keywords: {keywords}")]
        )

        # Run the workflow
        events = runner.run_async(
            user_id=user_id,
            session_id=session.id,
            new_message=content
        )
        
        # Collect all events and get the final result
        result_text = ""
        async for event in events:
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        result_text += part.text
        
        # Create a result-like object with the collected text
        result = Content(
            role="model",
            parts=[Part.from_text(text=result_text)]
        )

        logger.info(f"Workflow completed for user {user_id}")
        return result
        
    except Exception as e:
        logger.error(f"Failed to run workflow for user {user_id}: {e}")
        raise

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    """
    WebSocket endpoint for real-time story generation
    
    Args:
        websocket: WebSocket connection
        user_id: Unique user identifier
    """
    await websocket.accept()
    logger.info(f"Client #{user_id} connected")

    try:
        # Send connection confirmation
        await websocket.send_text(json.dumps({
            "type": "connected",
            "message": "Connected to StoryGen backend"
        }))

        while True:
            # Receive message from client
            message_json = await websocket.receive_text()
            message = json.loads(message_json)
            
            message_type = message.get("type")
            data = message.get("data", "")
            
            if message_type == "generate_story":
                try:
                    # Send processing notification
                    await websocket.send_text(json.dumps({
                        "type": "processing",
                        "message": "Generating story and images..."
                    }))
                    
                    # Run the workflow
                    result = await run_story_workflow(user_id, data)
                    logger.info(f"Workflow result type: {type(result)}")
                    logger.info(f"Workflow result parts: {len(result.parts) if result.parts else 0}")
                    
                    # Extract content from result
                    response_text = ""
                    for part in result.parts:
                        if part.text:
                            response_text += part.text
                    
                    logger.info(f"Extracted response text length: {len(response_text)}")
                    logger.info(f"Response text preview: {response_text[:200]}...")
                    
                    # Always send the story first, regardless of images
                    if response_text.strip():
                        logger.info(f"Sending story to frontend: {len(response_text)} chars")
                        await websocket.send_text(json.dumps({
                            "type": "story_complete",
                            "data": response_text.strip()
                        }))
                    else:
                        logger.warning("Empty response text from workflow")
                        await websocket.send_text(json.dumps({
                            "type": "error",
                            "message": "No story was generated"
                        }))
                    
                    # Check for image data separately
                    if "images" in response_text and "base64" in response_text:
                        logger.info("Found image data in response, parsing...")
                        try:
                            # Extract JSON from the response
                            json_start = response_text.find("{")
                            json_end = response_text.rfind("}") + 1
                            if json_start >= 0 and json_end > json_start:
                                json_data = json.loads(response_text[json_start:json_end])
                                
                                # Send images
                                if "images" in json_data:
                                    for image in json_data["images"]:
                                        await websocket.send_text(json.dumps({
                                            "type": "image_generated",
                                            "data": image
                                        }))
                                        logger.info(f"Sent image keyframe {image.get('keyframe', 'unknown')}")
                        except json.JSONDecodeError as e:
                            logger.error(f"Failed to parse image JSON: {e}")
                    else:
                        logger.info("No image data found in response")
                    
                    # Send completion notification
                    await websocket.send_text(json.dumps({
                        "type": "turn_complete",
                        "turn_complete": True,
                        "interrupted": False
                    }))
                    
                except Exception as e:
                    logger.error(f"Error generating story for user {user_id}: {e}")
                    await websocket.send_text(json.dumps({
                        "type": "error",
                        "message": f"Story generation failed: {str(e)}"
                    }))
                
            elif message_type == "ping":
                # Handle ping/keepalive messages
                await websocket.send_text(json.dumps({"type": "pong"}))
                
            else:
                logger.warning(f"Unknown message type: {message_type}")

    except WebSocketDisconnect:
        logger.info(f"Client #{user_id} disconnected")
    except Exception as e:
        logger.error(f"WebSocket error for user {user_id}: {e}")
        try:
            await websocket.send_text(json.dumps({
                "type": "error",
                "message": f"Server error: {str(e)}"
            }))
        except:
            pass
    finally:
        logger.info(f"Client #{user_id} connection closed")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "storygen-backend"}

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "StoryGen Backend API", "version": "2.0.0", "workflow": "sequential"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 