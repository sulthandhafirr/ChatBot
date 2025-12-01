"""Flask app for Vercel deployment (lightweight version without ChromaDB)"""
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import re

# Simple in-memory knowledge base
knowledge_base = []

def load_system_prompt():
    """Load system prompt"""
    try:
        # Try multiple possible paths for Vercel
        import os
        base_dir = os.path.dirname(os.path.abspath(__file__))
        paths = [
            os.path.join(base_dir, 'system_prompt.txt'),
            'system_prompt.txt',
            './system_prompt.txt'
        ]
        for path in paths:
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    return f.read()
    except:
        pass
    return "Netiquette Software Assistant. Answer concisely.\n\nData:\n{context}"

def simple_similarity(query, text):
    """Simple keyword matching"""
    query_words = set(re.findall(r'\w+', query.lower()))
    text_words = set(re.findall(r'\w+', text.lower()))
    if not query_words:
        return 0
    overlap = len(query_words & text_words)
    return overlap / len(query_words)

def load_knowledge_base():
    """Load knowledge from data.txt"""
    global knowledge_base
    try:
        # Try multiple paths for Vercel
        import os
        base_dir = os.path.dirname(os.path.abspath(__file__))
        paths = [
            os.path.join(base_dir, 'knowledge_base', 'data.txt'),
            'knowledge_base/data.txt',
            './knowledge_base/data.txt'
        ]
        
        content = None
        for path in paths:
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                break
        
        if content:
            chunks = content.split('\n\n')
            knowledge_base = [chunk.strip()[:200] for chunk in chunks if chunk.strip()]
            print(f"Loaded {len(knowledge_base)} chunks")
        else:
            # Fallback: embed knowledge directly
            knowledge_base = [
                "Netiquette Software adalah perusahaan penyedia solusi bisnis berbasis cloud yang didirikan di Asia Tenggara dan telah beroperasi lebih dari 16 tahun sebagai layanan aplikasi bisnis cloud terb",
                "Perusahaan ini berkembang di Singapura, Malaysia, Indonesia, Filipina, Hong Kong, dan Thailand. Netiquette membantu perusahaan dari skala kecil hingga menengah mengelola proses bisnis secara efisi",
                "Visi utama Netiquette adalah memberikan solusi cloud premium dengan biaya terjangkau untuk UKM dan perusahaan yang sedang bertumbuh.",
                "Layanan utama meliputi Accounting Management System untuk pencatatan transaksi, buku besar, rekonsiliasi bank, pengelolaan pajak, multi-mata uang, dan laporan keuangan real-time.",
                "Inventory Management System mengelola stok terpusat, gudang multi-lokasi, pembelian, penjualan, supplier, kontrol produksi, picking, packing, batch, serial number, dan laporan pergerakan barang.",
                "CRM membantu mengelola hubungan pelanggan, pipeline penjualan, follow-up, dan analisis performa tim sales untuk meningkatkan efektivitas penjualan.",
                "Payroll dan HR mencakup penggajian otomatis, manajemen karyawan, cuti, klaim, lembur, struktur gaji, dan peraturan ketenagakerjaan lokal.",
                "POS System mendukung transaksi kasir, integrasi inventori otomatis, diskon, multi-outlet, histori pelanggan, dan laporan penjualan terintegrasi dengan akuntansi.",
                "Customized Cloud Solution menyediakan solusi khusus seperti penyesuaian workflow, integrasi API, koneksi e-commerce, marketplace, sistem produksi, manajemen proyek, dan otomatisasi bisnis.",
                "Sistem berbasis cloud dapat diakses via browser, laptop, tablet, dan mobile dengan keamanan berlapis, enkripsi, backup reguler, dan pembaruan otomatis.",
                "Model layanan meliputi free trial 30 hari, training, technical support, implementasi sistem, migrasi database, dan konsultasi bisnis.",
                "Target pasar adalah retail, distribusi, perdagangan, manufaktur kecil, layanan profesional, dan perusahaan ekspansi di ASEAN dengan dukungan lokal di setiap negara.",
                "Kontak: Email support@netiquette.com, Website www.netiquette.com, Telepon +65-1234-5678"
            ]
            print(f"Using embedded knowledge: {len(knowledge_base)} chunks")
    except Exception as e:
        print(f"Error loading knowledge: {e}")
        knowledge_base = []

def query_knowledge_base(query, n_results=1):
    """Query knowledge base"""
    if not knowledge_base:
        return []
    scored = [(chunk, simple_similarity(query, chunk)) for chunk in knowledge_base]
    scored.sort(key=lambda x: x[1], reverse=True)
    return [chunk for chunk, score in scored[:n_results] if score > 0]

def call_deepseek_api(messages):
    """Call DeepSeek API"""
    import requests
    api_key = os.getenv('DEEPSEEK_API_KEY')
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": "deepseek-chat",
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 300,
        "stop": ["\n\n", "**"]
    }
    try:
        response = requests.post("https://api.deepseek.com/v1/chat/completions", json=data, headers=headers)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {str(e)}"

app = Flask(__name__, static_folder='frontend')
CORS(app)

# Load knowledge base on startup
load_knowledge_base()

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
    context_chunks = query_knowledge_base(user_message, n_results=1)
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
    if not os.getenv('DEEPSEEK_API_KEY'):
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
        'documents_count': len(knowledge_base)
    })

# For Vercel
app = app
