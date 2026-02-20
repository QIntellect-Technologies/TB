"""
FAISS-Based Vector Store for TB Expert RAG System
GPU-accelerated, optimized for Windows, faster indexing
"""
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from typing import List, Dict
import os
import pickle

class FAISSVectorStore:
    def __init__(self, persist_directory=None):
        """Initialize FAISS vector store with GPU support"""
        if persist_directory is None:
            # Resolve relative to this script
            base_dir = os.path.dirname(os.path.abspath(__file__))
            self.persist_directory = os.path.join(base_dir, "vector_db_faiss")
        else:
            self.persist_directory = persist_directory
            
        os.makedirs(self.persist_directory, exist_ok=True)
        
        # Initialize embedding model
        print("🔄 Loading multilingual embedding model...")
        self.embedding_model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
        
        # Try to use GPU if available
        if faiss.get_num_gpus() > 0:
            print("✅ GPU detected! Using GPU acceleration")
            self.use_gpu = True
        else:
            print("📝 No GPU detected, using CPU")
            self.use_gpu = False
        
        print("✅ Embedding model loaded")
        
        # Initialize indices
        self.en_index = None
        self.ur_index = None
        self.en_metadata = []
        self.ur_metadata = []
        
        # Load existing indices if available
        self._load_indices()
    
    def _load_indices(self):
        """Load existing FAISS indices from disk or build from fallout datasets"""
        en_index_path = os.path.join(self.persist_directory, "english.index")
        ur_index_path = os.path.join(self.persist_directory, "urdu.index")
        en_meta_path = os.path.join(self.persist_directory, "english_metadata.pkl")
        ur_meta_path = os.path.join(self.persist_directory, "urdu_metadata.pkl")
        
        # Base directory for relative dataset paths
        # Assuming we are in /app/backend
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        dataset_dir = os.path.join(root_dir, "dataset")
        
        # Load English
        if os.path.exists(en_index_path):
            print("📂 Loading existing English index...")
            self.en_index = faiss.read_index(en_index_path)
            with open(en_meta_path, 'rb') as f:
                self.en_metadata = pickle.load(f)
            print(f"✅ Loaded {len(self.en_metadata)} English documents")
        else:
            print("⚠️ English index not found. Checking for dataset to re-index...")
            en_json = os.path.join(dataset_dir, "TB_QA_DATASET_ENGLISH.json")
            if os.path.exists(en_json):
                self.index_dataset(en_json, "English")
            else:
                print(f"❌ English dataset not found at {en_json}")
        
        # Load Urdu
        if os.path.exists(ur_index_path):
            print("📂 Loading existing Urdu index...")
            self.ur_index = faiss.read_index(ur_index_path)
            with open(ur_meta_path, 'rb') as f:
                self.ur_metadata = pickle.load(f)
            print(f"✅ Loaded {len(self.ur_metadata)} Urdu documents")
        else:
            print("⚠️ Urdu index not found. Checking for dataset to re-index...")
            ur_json = os.path.join(dataset_dir, "TB_QA_DATASET_URDU_100K.json")
            if os.path.exists(ur_json):
                 self.index_dataset(ur_json, "Urdu")
            else:
                print(f"❌ Urdu dataset not found at {ur_json}")
    
    def generate_embeddings(self, texts: List[str], batch_size: int = 32) -> np.ndarray:
        """Generate embeddings with batching"""
        embeddings = self.embedding_model.encode(
            texts, 
            batch_size=batch_size,
            show_progress_bar=True,
            convert_to_numpy=True
        )
        return embeddings.astype('float32')
    
    def index_dataset(self, dataset_path: str, language: str):
        """Index a Q&A dataset into FAISS"""
        print(f"\n📂 Loading {language} dataset from {dataset_path}...")
        
        with open(dataset_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        qa_pairs = data.get('qa_pairs', [])
        total = len(qa_pairs)
        print(f"📊 Found {total:,} Q&A pairs")
        
        # Prepare documents (combine Q+A for better semantic search)
        documents = [f"Q: {item['question']}\nA: {item['answer']}" for item in qa_pairs]
        
        # Prepare metadata
        metadata = [
            {
                "id": item['id'],
                "question": item['question'],
                "answer": item['answer'],
                "category": item.get('category', 'General'),
                "language": language
            }
            for item in qa_pairs
        ]
        
        # Generate embeddings (optimized batching)
        print(f"🔄 Generating embeddings for {total:,} documents...")
        embeddings = self.generate_embeddings(documents, batch_size=64)
        
        # Create FAISS index
        dimension = embeddings.shape[1]  # 768 for this model
        
        if language == "English":
            print("🔧 Building English FAISS index...")
            self.en_index = faiss.IndexFlatIP(dimension)  # Inner Product (cosine similarity)
            
            # Normalize embeddings for cosine similarity
            faiss.normalize_L2(embeddings)
            
            # Add to index
            self.en_index.add(embeddings)
            self.en_metadata = metadata
            
            # Save to disk
            faiss.write_index(self.en_index, os.path.join(self.persist_directory, "english.index"))
            with open(os.path.join(self.persist_directory, "english_metadata.pkl"), 'wb') as f:
                pickle.dump(self.en_metadata, f)
            
            print(f"✅ Indexed {total:,} English documents!")
        
        else:  # Urdu
            print("🔧 Building Urdu FAISS index...")
            self.ur_index = faiss.IndexFlatIP(dimension)
            
            # Normalize embeddings
            faiss.normalize_L2(embeddings)
            
            # Add to index
            self.ur_index.add(embeddings)
            self.ur_metadata = metadata
            
            # Save to disk
            faiss.write_index(self.ur_index, os.path.join(self.persist_directory, "urdu.index"))
            with open(os.path.join(self.persist_directory, "urdu_metadata.pkl"), 'wb') as f:
                pickle.dump(self.ur_metadata, f)
            
            print(f"✅ Indexed {total:,} Urdu documents!")
        
        return total
    
    def search(self, query: str, language: str = "English", top_k: int = 5) -> List[Dict]:
        """Search for relevant documents"""
        # Select index and metadata
        if language == "English":
            index = self.en_index
            metadata = self.en_metadata
        else:
            index = self.ur_index
            metadata = self.ur_metadata
        
        if index is None or len(metadata) == 0:
            return []
        
        # Generate query embedding
        query_embedding = self.generate_embeddings([query], batch_size=1)
        faiss.normalize_L2(query_embedding)
        
        # Search
        distances, indices = index.search(query_embedding, top_k)
        
        # Format results
        results = []
        for i, (dist, idx) in enumerate(zip(distances[0], indices[0])):
            if idx < len(metadata):
                result = metadata[idx].copy()
                result['relevance_score'] = float(dist)  # Cosine similarity (0-1)
                result['distance'] = float(1 - dist)
                results.append(result)
        
        return results

if __name__ == "__main__":
    import time
    
    # Initialize vector store
    vs = FAISSVectorStore()
    
    print("\n" + "="*60)
    print("🚀 INDEXING TB EXPERT DATASETS WITH FAISS")
    print("="*60)
    
    start_time = time.time()
    
    # Index English dataset
    en_count = vs.index_dataset("dataset/TB_QA_DATASET_ENGLISH.json", "English")
    
    # Index Urdu dataset
    ur_count = vs.index_dataset("dataset/TB_QA_DATASET_URDU_100K.json", "Urdu")
    
    elapsed = time.time() - start_time
    
    print("\n" + "="*60)
    print(f"✅ INDEXING COMPLETE!")
    print(f"📊 English: {en_count:,} documents")
    print(f"📊 Urdu: {ur_count:,} documents")
    print(f"⏱️  Total time: {elapsed/60:.1f} minutes")
    print("="*60)
    
    # Test search
    print("\n🧪 Testing semantic search...")
    test_query = "What are the symptoms of tuberculosis?"
    results = vs.search(test_query, language="English", top_k=3)
    
    print(f"\nQuery: {test_query}")
    print("\nTop 3 Results:")
    for i, result in enumerate(results, 1):
        print(f"\n{i}. [Score: {result['relevance_score']:.3f}] {result['category']}")
        print(f"   Q: {result['question'][:100]}...")
        print(f"   A: {result['answer'][:150]}...")
