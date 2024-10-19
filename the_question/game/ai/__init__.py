import json
from urllib import request, error
from enum import StrEnum
from typing import Optional

INFERENCE_HOST = "http://0.0.0.0:8080"
INFERENCE_ENDPOINT = "/api/message"

class Role(StrEnum):
    SYSTEM = "system"
    ASSISTANT = "assistant"
    USER = "user"
    
def message(user_input: str, messages: list[dict], candidate_labels: list[str]) -> tuple[Optional[str], list[dict], Optional[str]]:
    """Invokes LLM to generate a response to the user input. 
    
    Returns the classified label (if any), the updated list of messages for the next LLM call, and the prompt for the player to respond to.

    Args:
        user_input (str): The user's response to the last question.
        messages (list[Message]): The list of messages to pass to the LLM.
        candidate_labels (list[str]): The list of possible labels that the LLM may classify the user's response as.
    """
    
    # Validate input
    if not isinstance(candidate_labels, list) or not all((isinstance(label, str) and label) for label in candidate_labels):
        raise TypeError("candidate_labels must be a list of strings")
    if not user_input or not isinstance(user_input, str):
        raise TypeError("user_input must be a string")
    processed_messages: list[dict] = _process_messages(messages=messages)
    
            
    payload = {
        "user_input": user_input,
        "messages": processed_messages,
        "candidate_labels": candidate_labels
    }

    try:
        data = json.dumps(payload).encode('utf-8')
        req = request.Request(f"{INFERENCE_HOST}{INFERENCE_ENDPOINT}", data=data, method='POST')
        req.add_header('Content-Type', 'application/json')
        
        with request.urlopen(req) as response:
            response_data = response.read().decode('utf-8')
            data = json.loads(response_data)
            classified_label = data.get("classified_label")
            messages = data.get("messages")
            prompt = data.get("prompt")
            
            return classified_label, messages, prompt
            
            
    except error.URLError as e:
        raise RuntimeError(f"Failed to call inference endpoint: {e}")
    
def _process_messages(messages: list[dict]) -> list[dict]:
    """Processes the messages sent from the renpy client to make sure that it conforms to the expected format."""
    processed_messages: list[dict] = []
    for message in messages:
        if len(message) > 1:
            raise ValueError("Each dictionary in the messages list should only contain one key-value pair")
        
        original_key = list(message.keys())[0]
        processed_key = original_key.strip().lower()
        modified_dict: dict[str, str] = {}
        
        if processed_key == Role.SYSTEM:
            modified_dict["role"] = Role.SYSTEM
        elif processed_key == Role.ASSISTANT:
            modified_dict["role"] = Role.ASSISTANT
        elif processed_key == Role.USER:
            modified_dict["role"] = Role.USER
        else:
            raise ValueError(f"Invalid key {processed_key} in message. Expected one of {Role.__members__}")
        
        value: str = message[original_key]
        if not value or not isinstance(value, str):
            raise ValueError(f"Value for key {processed_key} in message must be a string")
        
        modified_dict["content"] = value
        
        processed_messages.append(modified_dict)
    
    return processed_messages