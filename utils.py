"""Utility functions"""
from config import SYSTEM_PROMPT_FILE

def load_system_prompt():
    """Load system prompt from file"""
    try:
        with open(SYSTEM_PROMPT_FILE, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Warning: {SYSTEM_PROMPT_FILE} not found!")
        return "Kamu adalah asisten virtual yang membantu."
