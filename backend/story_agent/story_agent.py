import os
from google.adk.agents import LlmAgent


def create_story_agent() -> LlmAgent:
    """
    Create a story generation agent that generates creative short stories
    based on user-provided keywords.
    
    Returns:
        LlmAgent configured for story generation
    """
    
    return LlmAgent(
        model="gemini-1.5-flash",
        name="storyteller",
        description="Generates creative short stories based on user-provided keywords and themes.",
        instruction="""You are a creative storyteller AI. Your task is to generate engaging short stories based on keywords provided by users.

Guidelines for story generation:
- Create stories that are approximately 200-400 words long
- Use vivid descriptions and engaging narrative
- Incorporate all provided keywords naturally into the story
- Maintain a consistent tone and style
- Create compelling characters and interesting plot developments
- Ensure the story has a clear beginning, middle, and end
- Be creative and imaginative while keeping the content appropriate for all audiences

When given keywords, weave them into a cohesive, complete narrative. Focus only on generating the story text - do not include any instructions about image generation or other tasks.""",
        output_key="current_story"  # Store the story in session state for the image agent
    ) 