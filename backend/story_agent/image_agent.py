import os
import json
import re
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel
from google.adk.agents import BaseAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events.event import Event
from google.genai.types import Content, Part
from typing import AsyncGenerator


class ImageGenerationAgent(BaseAgent):
    """
    ADK Agent for generating images using Google Vertex AI Imagen.
    
    This agent takes story text as input and generates visual keyframes
    representing key moments in the story.
    """
    
    # Declare class attributes for Pydantic
    _project_id: str
    _location: str
    _model: ImageGenerationModel
    
    # Allow arbitrary types for Pydantic
    model_config = {"arbitrary_types_allowed": True}
    
    def __init__(self, name: str = "image_generator", project_id: str = None, location: str = "us-central1"):
        # Call BaseAgent constructor first
        super().__init__(
            name=name,
            description="ADK Agent for generating images using Google Vertex AI Imagen",
            sub_agents=[]  # No sub-agents for this custom agent
        )
        
        # Then initialize our custom attributes
        self._project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT_ID")
        self._location = location
        
        if not self._project_id:
            raise ValueError("Google Cloud Project ID not configured. Please set GOOGLE_CLOUD_PROJECT_ID environment variable.")
        
        # Initialize Vertex AI
        vertexai.init(project=self._project_id, location=self._location)
        self._model = ImageGenerationModel.from_pretrained("imagegeneration@006")
    

    
    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
        """
        Process the input story and generate visual keyframes.
        
        Args:
            ctx: InvocationContext containing session state and other context
            
        Yields:
            Events with generated image data
        """
        try:
            # Extract story text from session state (set by the story agent)
            story_text = ctx.session.state.get("current_story", "")
            
            if not story_text.strip():
                error_content = Content(
                    role="model",
                    parts=[Part.from_text(text="Error: No story text found in session state for image generation.")]
                )
                yield Event(author=self.name, content=error_content)
                return
            
            # Extract key scenes from the story for image generation
            image_prompts = self._extract_image_prompts(story_text)
            
            # Generate images for each prompt
            generated_images = []
            for i, prompt in enumerate(image_prompts):
                try:
                    images = self._model.generate_images(
                        prompt=prompt,
                        number_of_images=1,
                        negative_prompt="cartoon, sketch, drawing, low quality, blurry",
                        aspect_ratio="16:9"
                    )
                    
                    # Convert to base64 (similar to existing tool)
                    import tempfile
                    import base64
                    
                    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
                        images[0].save(location=temp_file.name)
                        
                        with open(temp_file.name, "rb") as img_file:
                            img_base64 = base64.b64encode(img_file.read()).decode('utf-8')
                            generated_images.append({
                                "keyframe": i + 1,
                                "prompt": prompt,
                                "base64": img_base64,
                                "format": "png"
                            })
                        
                        os.unlink(temp_file.name)
                        
                except Exception as e:
                    generated_images.append({
                        "keyframe": i + 1,
                        "prompt": prompt,
                        "error": f"Failed to generate image: {str(e)}"
                    })
            
            # Store results in session state and create response
            result = {
                "success": True,
                "story_analyzed": True,
                "keyframes_generated": len(generated_images),
                "images": generated_images
            }
            
            # Store in session state for other agents to access
            ctx.session.state["image_generation_result"] = result
            
            response_text = f"✅ Successfully generated {len(generated_images)} visual keyframes for the story.\n\n"
            response_text += json.dumps(result, indent=2)
            
            response_content = Content(
                role="model",
                parts=[Part.from_text(text=response_text)]
            )
            yield Event(author=self.name, content=response_content)
            
        except Exception as e:
            error_message = f"❌ Image generation failed: {str(e)}"
            error_content = Content(
                role="model",
                parts=[Part.from_text(text=error_message)]
            )
            yield Event(author=self.name, content=error_content)
    
    def _extract_image_prompts(self, story_text: str) -> list[str]:
        """
        Extract 4 key visual moments from the story text to create image prompts.
        
        Args:
            story_text: The complete story text
            
        Returns:
            List of 4 detailed image generation prompts
        """
        # Split story into sentences for analysis
        sentences = re.split(r'[.!?]+', story_text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # Create 4 keyframes representing story progression
        total_sentences = len(sentences)
        
        if total_sentences < 4:
            # For short stories, use all sentences
            keyframe_sentences = sentences
        else:
            # Select sentences from beginning, early middle, late middle, and end
            indices = [
                0,  # Beginning
                total_sentences // 3,  # Early middle
                (2 * total_sentences) // 3,  # Late middle
                total_sentences - 1  # End
            ]
            keyframe_sentences = [sentences[i] for i in indices]
        
        # Convert sentences to detailed image prompts
        prompts = []
        scene_types = ["opening scene", "rising action", "climax", "resolution"]
        
        for i, sentence in enumerate(keyframe_sentences):
            scene_type = scene_types[min(i, len(scene_types) - 1)]
            
            # Create detailed cinematic prompt
            prompt = f"Cinematic {scene_type}: {sentence}. "
            prompt += "Photorealistic, dramatic lighting, high detail, cinematic composition, "
            prompt += "professional photography style, atmospheric mood"
            
            prompts.append(prompt)
        
        # Ensure we always return 4 prompts
        while len(prompts) < 4:
            prompts.append(prompts[-1] if prompts else "A beautiful cinematic scene, photorealistic, dramatic lighting")
        
        return prompts[:4] 