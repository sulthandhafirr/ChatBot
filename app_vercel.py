"""Flask app for Vercel deployment (lightweight version without ChromaDB)"""
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import lightweight database
import database_light as database
from api_client import call_deepseek_api
from utils import load_system_prompt

app = Flask(__name__, static_folder='frontend')
CORS(app)

# Configuration
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
CONTEXT_CHUNKS = 1

# Load knowledge base on startup
database.load_knowledge_base()

@app.route('/')
def index():
    """Serve frontend"""
    return send_from_directory('frontend', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files"""
    return send_from_directory('frontend', path)

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat requests"""
    data = request.json
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({'error': 'Message is required'}), 400
    
    # Retrieve relevant context
    context_chunks = database.query_knowledge_base(user_message, n_results=CONTEXT_CHUNKS)
    context = "\n\n".join(context_chunks) if context_chunks else ""
    
    # Load system prompt
    system_prompt = load_system_prompt()
    
    # Build messages
    messages = [
        {
            "role": "system",
            "content": system_prompt.format(context=context)
        },
        {
            "role": "user",
            "content": user_message
        }
    ]
    
    # Get response
    if not DEEPSEEK_API_KEY:
        return jsonify({'error': 'API key not configured'}), 500
    
    response = call_deepseek_api(messages)
    
    return jsonify({
        'response': response,
        'context_used': len(context_chunks)
    })

@app.route('/api/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({
        'status': 'healthy',
        'documents_count': database.get_documents_count()
    })

# For Vercel
app = app
