"""Simple in-memory knowledge base (no ChromaDB for Vercel deployment)"""
from pathlib import Path
from config import KNOWLEDGE_BASE_DIR
import re

# Store knowledge base in memory
knowledge_base = []

def load_knowledge_base(force_reload=False):
    """Load knowledge base files into memory"""
    global knowledge_base
    
    if knowledge_base and not force_reload:
        print(f"Knowledge base already loaded: {len(knowledge_base)} documents")
        return
    
    knowledge_dir = Path(KNOWLEDGE_BASE_DIR)
    if not knowledge_dir.exists():
        print("Knowledge base directory not found!")
        return
    
    knowledge_base = []
    for file_path in knowledge_dir.glob("*.txt"):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split into chunks
        chunks = content.split('\n\n')
        for chunk in chunks:
            chunk = chunk.strip()
            if chunk:
                # Limit to 200 chars
                if len(chunk) > 200:
                    chunk = chunk[:200]
                knowledge_base.append(chunk)
    
    print(f"Loaded {len(knowledge_base)} chunks into memory")

def simple_similarity(query, text):
    """Simple keyword-based similarity"""
    query_words = set(re.findall(r'\w+', query.lower()))
    text_words = set(re.findall(r'\w+', text.lower()))
    
    if not query_words:
        return 0
    
    # Calculate overlap
    overlap = len(query_words & text_words)
    return overlap / len(query_words)

def query_knowledge_base(query, n_results=1):
    """Query knowledge base using simple keyword matching"""
    if not knowledge_base:
        load_knowledge_base()
    
    # Score each chunk
    scored = [(chunk, simple_similarity(query, chunk)) for chunk in knowledge_base]
    
    # Sort by score and get top results
    scored.sort(key=lambda x: x[1], reverse=True)
    
    return [chunk for chunk, score in scored[:n_results] if score > 0]

def get_documents_count():
    """Get total number of documents"""
    return len(knowledge_base)
