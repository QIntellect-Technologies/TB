"""
Vector Store Manager for TB Expert RAG System
Handles embedding generation and vector database operations
"""
import json
import chromadb
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Tuple
import os

class VectorStore:
    def __init__(self, persist_directory="backend/vector_db"):
        """Initialize vector store with ChromaDB and embedding model"""
        self.persist_directory = persist_directory
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # Load embedding model (multilingual for English + Urdu)
        print("🔄 Loading multilingual embedding model...")
        self.embedding_model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
        print("✅ Embedding model loaded")
        
        # Get or create collections
        self.en_collection = self.client.get_or_create_collection(
            name="tb_expert_english",
            metadata={"language": "English"}
        )
        
        self.ur_collection = self.client.get_or_create_collection(
            name="tb_expert_urdu",
            metadata={"language": "Urdu"}
        )
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of texts"""
        embeddings = self.embedding_model.encode(texts, show_progress_bar=True)
        return embeddings.tolist()
    
    def index_dataset(self, dataset_path: str, language: str):
        """Index a Q&A dataset into the vector store"""
        print(f"\n📂 Loading {language} dataset from {dataset_path}...")
        
        with open(dataset_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        qa_pairs = data.get('qa_pairs', [])
        total = len(qa_pairs)
        print(f"📊 Found {total:,} Q&A pairs")
        
        # Select collection
        collection = self.en_collection if language == "English" else self.ur_collection
        
        # Check if already indexed
        existing_count = collection.count()
        if existing_count > 0:
            print(f"⚠️  Collection already has {existing_count:,} documents. Clearing...")
            self.client.delete_collection(collection.name)
            collection = self.client.create_collection(
                name=collection.name,
                metadata={"language": language}
            )
        
        # Process in batches
        batch_size = 1000
        for i in range(0, total, batch_size):
            batch = qa_pairs[i:i+batch_size]
            
            # Prepare data
            ids = [item['id'] for item in batch]
            questions = [item['question'] for item in batch]
            answers = [item['answer'] for item in batch]
            categories = [item.get('category', 'General') for item in batch]
            
            # Combine question + answer for better semantic search
            documents = [f"Q: {q}\nA: {a}" for q, a in zip(questions, answers)]
            
            # Generate embeddings
            print(f"🔄 Processing batch {i//batch_size + 1}/{(total-1)//batch_size + 1}...")
            embeddings = self.generate_embeddings(documents)
            
            # Add to collection
            collection.add(
                ids=ids,
                embeddings=embeddings,
                documents=documents,
                metadatas=[{
                    "question": q,
                    "answer": a,
                    "category": c,
                    "language": language
                } for q, a, c in zip(questions, answers, categories)]
            )
        
        print(f"✅ Indexed {total:,} {language} documents successfully!")
        return total
    
    def search(self, query: str, language: str = "English", top_k: int = 5) -> List[Dict]:
        """Search for relevant documents"""
        # Select collection
        collection = self.en_collection if language == "English" else self.ur_collection
        
        # Generate query embedding
        query_embedding = self.generate_embeddings([query])[0]
        
        # Search
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        # Format results
        formatted_results = []
        if results['metadatas'] and len(results['metadatas'][0]) > 0:
            for i, metadata in enumerate(results['metadatas'][0]):
                formatted_results.append({
                    "question": metadata['question'],
                    "answer": metadata['answer'],
                    "category": metadata['category'],
                    "distance": results['distances'][0][i] if results['distances'] else 0,
                    "relevance_score": 1 - results['distances'][0][i] if results['distances'] else 1.0
                })
        
        return formatted_results

if __name__ == "__main__":
    # Initialize vector store
    vs = VectorStore()
    
    # Index datasets
    print("\n" + "="*60)
    print("🚀 INDEXING TB EXPERT DATASETS FOR RAG")
    print("="*60)
    
    en_count = vs.index_dataset("dataset/TB_QA_DATASET_ENGLISH.json", "English")
    ur_count = vs.index_dataset("dataset/TB_QA_DATASET_URDU_100K.json", "Urdu")
    
    print("\n" + "="*60)
    print(f"✅ INDEXING COMPLETE!")
    print(f"📊 English: {en_count:,} documents")
    print(f"📊 Urdu: {ur_count:,} documents")
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
