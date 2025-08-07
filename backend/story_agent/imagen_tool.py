import os
import base64
import tempfile
from typing import List, Optional, Dict, Any
import json
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel
from google.adk.tools import FunctionTool


def generate_image(
    prompt: str,
    negative_prompt: Optional[str] = None,
    aspect_ratio: Optional[str] = "16:9",
    number_of_images: Optional[int] = 1
) -> str:
    """Generate images using Google Imagen based on text prompts. Perfect for creating visual representations of story scenes, characters, or key moments.
    
    Args:
        prompt: Detailed text description of the image to generate. Be specific about style, mood, objects, characters, and setting.
        negative_prompt: Optional description of what to exclude from the image (e.g., 'cartoon, drawing, sketch' for photorealistic images)
        aspect_ratio: Aspect ratio for the generated image. Options: '1:1', '16:9', '9:16', '4:3', '3:4'
        number_of_images: Number of images to generate (1-4)
        
    Returns:
        JSON string with image data (base64 encoded images)
    """
    try:
        # Get project ID from environment
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
        if not project_id:
            return json.dumps({
                "success": False,
                "error": "Google Cloud Project ID not configured. Please set GOOGLE_CLOUD_PROJECT_ID in your .env file."
            })
        
        # Validate inputs
        if not prompt or not prompt.strip():
            return json.dumps({"success": False, "error": "Prompt cannot be empty"})
        
        # Ensure number_of_images is within bounds
        number_of_images = max(1, min(4, number_of_images or 1))
        
        # Validate aspect ratio
        valid_ratios = ["1:1", "16:9", "9:16", "4:3", "3:4"]
        if aspect_ratio not in valid_ratios:
            aspect_ratio = "16:9"
        
        # Initialize Vertex AI
        vertexai.init(project=project_id, location="us-central1")
        
        # Load the Imagen model
        model = ImageGenerationModel.from_pretrained("imagegeneration@006")
        
        # Generate images
        images = model.generate_images(
            prompt=prompt,
            number_of_images=number_of_images,
            negative_prompt=negative_prompt,
            aspect_ratio=aspect_ratio
        )
        
        # Convert images to base64
        image_data = []
        for i, image in enumerate(images):
            # Save image to temporary file
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
                image.save(location=temp_file.name)
                
                # Read and encode as base64
                with open(temp_file.name, "rb") as img_file:
                    img_base64 = base64.b64encode(img_file.read()).decode('utf-8')
                    image_data.append({
                        "index": i,
                        "base64": img_base64,
                        "format": "png"
                    })
                
                # Clean up temp file
                os.unlink(temp_file.name)
        
        result = {
            "success": True,
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "aspect_ratio": aspect_ratio,
            "images": image_data
        }
        
        return json.dumps(result)
        
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": f"Image generation failed: {str(e)}"
        })


def create_imagen_tool() -> FunctionTool:
    """
    Factory function to create an Imagen tool instance
    
    Returns:
        FunctionTool instance for image generation
    """
    return FunctionTool(func=generate_image) 