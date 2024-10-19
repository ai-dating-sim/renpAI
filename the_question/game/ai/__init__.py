from enum import StrEnum
from typing import Optional

class Role(StrEnum):
    SYSTEM = "system"
    ASSISTANT = "assistant"
    USER = "user"
    
def call(user_input: str, messages: list[dict], candidate_labels: list[str]) -> tuple[Optional[str], list[dict], Optional[str]]:
    """Invokes LLM to generate a response to the user input. 
    
    Returns the classified label (if any), the updated list of messages for the next LLM call, and the prompt for the player to respond to.

    Args:
        user_input (str): The user's response to the last question.
        messages (list[Message]): The list of messages to pass to the LLM.
        candidate_labels (list[str]): The list of possible labels that the LLM may classify the user's response as.
    """
    processed_messages = []
    for message in messages:
        if len(message) > 1:
            raise ValueError("Each dictionary in the messages list should only contain one key-value pair")
        
        original_key = list(message.keys())[0]
        processed_key = original_key.strip().upper()            
        if processed_key not in Role.__members__:
            raise ValueError(f"Invalid key {processed_key} in message. Expected one of {Role.__members__}")
        processed_messages.append({processed_key.lower(): message[original_key]})
            
            
    # TODO: Call endpoint
    return user_input, processed_messages, "What do you say?"