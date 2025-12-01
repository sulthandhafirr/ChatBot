"""ChromaDB database operations"""
import chromadb
from chromadb.utils import embedding_functions
from pathlib import Path
from config import CHROMA_DB_PATH, COLLECTION_NAME, KNOWLEDGE_BASE_DIR

# Initialize ChromaDB
chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)

# Use default embedding function
default_ef = embedding_functions.DefaultEmbeddingFunction()

# Get or create collection
collection = chroma_client.get_or_create_collection(
    name=COLLECTION_NAME,
    embedding_function=default_ef
)

def load_knowledge_base(force_reload=False):
    """Load knowledge base files into ChromaDB"""
    knowledge_dir = Path(KNOWLEDGE_BASE_DIR)
    
    if not knowledge_dir.exists():
        print("Knowledge base directory not found!")
        return
    
    # Check if collection already has documents
    if collection.count() > 0:
        if force_reload:
            print(f"Force reload: Clearing {collection.count()} existing documents...")
            existing_ids = collection.get()['ids']
            if existing_ids:
                collection.delete(ids=existing_ids)
            print("✓ Collection cleared")
        else:
            print(f"Collection already has {collection.count()} documents. Skipping load.")
            return
    
    documents = []
    metadatas = []
    ids = []
    
    for file_path in knowledge_dir.glob("*.txt"):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Split content into chunks (max 300 chars per chunk to save tokens)
        chunks = content.split('\n\n')
        
        for i, chunk in enumerate(chunks):
            chunk = chunk.strip()
            if chunk:
                # Limit chunk size to 200 characters
                if len(chunk) > 200:
                    chunk = chunk[:200]
                documents.append(chunk)
                metadatas.append({
                    "source": file_path.stem,
                    "chunk_id": i
                })
                ids.append(f"{file_path.stem}_{i}")
    
    if documents:
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        print(f"Loaded {len(documents)} chunks into ChromaDB")

def query_knowledge_base(query, n_results=3):
    """Query ChromaDB for relevant context"""
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    
    if results and results['documents']:
        return results['documents'][0]
    return []

def get_documents_count():
    """Get total number of documents in collection"""
    return collection.count()
