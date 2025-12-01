"""Main Flask application for Netiquette Software Chatbot"""
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from config import DEEPSEEK_API_KEY, HOST, PORT, DEBUG, CONTEXT_CHUNKS
from database import load_knowledge_base, query_knowledge_base, get_documents_count
from api_client import call_deepseek_api
from utils import load_system_prompt

app = Flask(__name__, static_folder='frontend')
CORS(app)

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
    
    # Retrieve relevant context from knowledge base
    context_chunks = query_knowledge_base(user_message, n_results=CONTEXT_CHUNKS)
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
    
    # Get response from DeepSeek API
    if not DEEPSEEK_API_KEY:
        return jsonify({'error': 'DeepSeek API key not configured'}), 500
    
    response = call_deepseek_api(messages)
    
    return jsonify({
        'response': response,
        'context_used': len(context_chunks)
    })

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'documents_count': get_documents_count()
    })

if __name__ == '__main__':
    print("\n" + "="*50)
    print("   NETIQUETTE SOFTWARE CHATBOT")
    print("="*50 + "\n")
    
    # Check API key
    if not DEEPSEEK_API_KEY or DEEPSEEK_API_KEY == 'your_deepseek_api_key_here':
        print("✗ WARNING: DeepSeek API key belum dikonfigurasi!")
        print("  Edit file .env dan isi DEEPSEEK_API_KEY")
        print("")
    else:
        print("✓ DeepSeek API key configured")
    
    # Load knowledge base on startup
    load_knowledge_base(force_reload=True)
    
    print(f"\n✓ Knowledge base loaded: {get_documents_count()} documents")
    print(f"✓ Server URL: http://localhost:{PORT}")
    print("\n" + "="*50)
    print("   SERVER STARTING...")
    print("="*50 + "\n")
    
    app.run(debug=DEBUG, host=HOST, port=PORT)
