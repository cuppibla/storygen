import os
from google.adk.agents import SequentialAgent
from .story_agent import create_story_agent
from .image_agent import ImageGenerationAgent


def create_story_workflow_agent() -> SequentialAgent:
    """
    Create a sequential workflow agent that:
    1. Generates a story from keywords using LLM
    2. Generates visual keyframes from the story using Imagen
    
    Returns:
        SequentialAgent configured for story-to-image workflow
    """
    
    # Create the story generation agent
    story_agent = create_story_agent()
    
    # Create the image generation agent (only if project ID is available)
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    sub_agents = [story_agent]
    
    # Create the image generation agent (only if project ID is available)
    if project_id:
        try:
            image_agent = ImageGenerationAgent(
                name="image_generator",
                project_id=project_id
            )
            sub_agents.append(image_agent)
            print("✅ Image generation agent added to workflow")
        except Exception as e:
            print(f"⚠️  Warning: Could not initialize image generation agent: {e}")
            print("📝 Story generation will work without images")
    else:
        print("💡 To enable image generation, set GOOGLE_CLOUD_PROJECT_ID in your .env file")
    
    # Create sequential workflow
    workflow_agent = SequentialAgent(
        name="story_to_image_workflow",
        description="Sequential workflow that generates stories and accompanying visual keyframes",
        sub_agents=sub_agents
    )
    
    return workflow_agent 