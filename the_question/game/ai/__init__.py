import json
from urllib import request, error
from enum import StrEnum
from typing import Optional
import ssl

INFERENCE_HOST = "https://renpai.duckdns.org:8080"
INFERENCE_ENDPOINT = "/api/message"

context = ssl._create_unverified_context()

# TODO: Hardcoded for now, will need to populate from .env variable
API_KEY = "your-api-key"

class Role(StrEnum):
    SYSTEM = "system"
    ASSISTANT = "assistant"
    USER = "user"
    
def message(character_profile: str, prompt: str, user_input: str, messages: list[dict], possible_images: list[str], possible_labels: list[str]) -> tuple[Optional[str], list[dict], Optional[str]]:
    """Invokes LLM to generate a response to the user input. 
    
    Returns the classified label (if any), the updated list of messages for the next LLM call, and the prompt for the player to respond to.

    Args:
        prompt (str): The prompt for the player to respond to.
        user_input (str): The user's response to the prompt.
        messages (list[Message]): The list of messages between the player and the visual novel character.
        possible_images (list[str]): The list of possible images that the LLM may choose to pair with the conversation.
        possible_lables (list[str]): The list of possible labels that the LLM may classify the user's response as.
    """
    
    # Validate input
    if not character_profile or not isinstance(character_profile, str):
        raise TypeError("character_profile must be a string")
    if not prompt or not isinstance(prompt, str):
        raise TypeError("prompt must be a string")
    if not user_input or not isinstance(user_input, str):
        raise TypeError("user_input must be a string")
    if not possible_images or not isinstance(possible_images, list) or not all((isinstance(image, str) and image) for image in possible_images):
        raise TypeError("possible_images must be a list of strings")
    if not possible_labels or not isinstance(possible_labels, list) or not all((isinstance(label, str) and label) for label in possible_labels):
        raise TypeError("possible_lables must be a list of strings")
    if not isinstance(messages, list) or not all((isinstance(message, dict) and message) for message in messages):
        raise TypeError("messages must be a list of dictionaries")
    
    messages.extend([
        {
            "role": "assistant",
            "content": prompt
        },
        {
            "role": "user",
            "content": user_input
        }
    ])

    payload = {
        "character_profile": character_profile,
        "messages": messages,
        "possible_images": possible_images,
        "possible_labels": possible_labels,
    }

    try:
        data = json.dumps(payload).encode('utf-8')
        req = request.Request(f"{INFERENCE_HOST}{INFERENCE_ENDPOINT}", data=data, method='POST')
        req.add_header('Content-Type', 'application/json')
        req.add_header('X-API-Key', API_KEY)
        
        with request.urlopen(req, context=context) as response:
            response_data = response.read().decode('utf-8')
            data = json.loads(response_data)
            image = data.get("image")
            classified_label = data.get("classified_label")
            prompt = data.get("prompt")
            
            return image, classified_label, messages, prompt
            
            
    except error.URLError as e:
        raise RuntimeError(f"Failed to call inference endpoint: {e}")
    