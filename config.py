"""Configuration settings for the chatbot application"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

# Server Configuration
HOST = '0.0.0.0'
PORT = 5000
DEBUG = True

# Database Configuration
CHROMA_DB_PATH = "./chroma_db"
COLLECTION_NAME = "personal_knowledge"

# Knowledge Base Configuration
KNOWLEDGE_BASE_DIR = "knowledge_base"
SYSTEM_PROMPT_FILE = "system_prompt.txt"

# API Parameters
TEMPERATURE = 0.7
MAX_TOKENS = 300
CONTEXT_CHUNKS = 1
