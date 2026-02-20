"""
Incremental FAISS Indexing (Fixed)
Adds new questions to existing FAISS index without re-indexing everything.
Supports both List and Dict {"qa_pairs": []} JSON formats.
"""
import json
import pickle
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import os
from tqdm import tqdm

class IncrementalIndexer:
    def __init__(self):
        self.model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
        self.dimension = 768
        
        # Paths - MATCHING vector_store_faiss.py
        self.index_dir = "backend/vector_db_faiss"
        if not os.path.exists(self.index_dir):
            # Fallback for old path
            self.index_dir = "backend/faiss_index"
            
        print(f"📂 Index Directory: {self.index_dir}")
        
        # Load existing indices and metadata
        self.english_index = None
        self.urdu_index = None
        self.english_metadata = []
        self.urdu_metadata = []
        
    def load_existing_indices(self):
        """Load existing FAISS indices and metadata"""
        print("\n📂 Loading existing indices...")
        
        # Load English
        en_index_path = os.path.join(self.index_dir, "english.index")
        en_meta_path = os.path.join(self.index_dir, "english_metadata.pkl")
        
        if os.path.exists(en_index_path):
            self.english_index = faiss.read_index(en_index_path)
            with open(en_meta_path, 'rb') as f:
                self.english_metadata = pickle.load(f)
            print(f"✅ Loaded English index: {self.english_index.ntotal} documents")
        else:
            print("❌ English index not found!")
            # Don't return False here, try to load Urdu at least
        
        # Load Urdu
        ur_index_path = os.path.join(self.index_dir, "urdu.index")
        ur_meta_path = os.path.join(self.index_dir, "urdu_metadata.pkl")
        
        if os.path.exists(ur_index_path):
            self.urdu_index = faiss.read_index(ur_index_path)
            with open(ur_meta_path, 'rb') as f:
                self.urdu_metadata = pickle.load(f)
            print(f"✅ Loaded Urdu index: {self.urdu_index.ntotal} documents")
        else:
            print("❌ Urdu index not found!")
            
        return (self.english_index is not None) or (self.urdu_index is not None)
    
    def get_new_questions(self, json_file, existing_metadata):
        """Get only NEW questions that aren't in existing metadata"""
        print(f"\n🔍 Checking for new questions in {json_file}...")
        
        if not os.path.exists(json_file):
            print(f"❌ File not found: {json_file}")
            return []
            
        # Load JSON (Handle both List and Dict formats)
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        if isinstance(data, dict):
            all_questions = data.get("qa_pairs", [])
        elif isinstance(data, list):
            all_questions = data
        else:
            print("❌ Unknown JSON format")
            return []
        
        # Create a set of existing questions (normalized)
        existing_questions = set()
        for meta in existing_metadata:
            if 'question' in meta:
                existing_questions.add(meta['question'].strip().lower())
        
        # Filter new questions
        new_questions = []
        for q in all_questions:
            q_text = q.get('question', '').strip().lower()
            if q_text and q_text not in existing_questions:
                # Add metadata fields needed for index
                q_obj = {
                    "id": q.get('id', f"NEW_{len(new_questions)}"),
                    "question": q.get('question', ''),
                    "answer": q.get('answer', ''),
                    "category": q.get('category', 'General')
                }
                new_questions.append(q_obj)
        
        print(f"📊 Total in JSON: {len(all_questions)}")
        print(f"📊 Already indexed: {len(existing_questions)}")
        print(f"✨ NEW questions to add: {len(new_questions)}")
        
        return new_questions
    
    def add_to_index(self, new_questions, language="English"):
        """Add new questions to existing index"""
        if not new_questions:
            print(f"⚠️  No new {language} questions to add!")
            return
        
        print(f"\n{'='*80}")
        print(f"🔄 Adding {len(new_questions)} NEW {language} questions to index")
        print(f"{'='*80}")
        
        # Select index and metadata
        if language == "English":
            index = self.english_index
            metadata = self.english_metadata
        else:
            index = self.urdu_index
            metadata = self.urdu_metadata
            
        if index is None:
            print(f"❌ Index not loaded for {language}")
            return
        
        # Generate embeddings or batch them
        print(f"\n🧠 Generating embeddings...")
        questions_text = [q['question'] for q in new_questions]
        
        # Prepare 'documents' (this normally includes Q and A)
        # In vector_store_faiss.py: documents = [f"Q: {item['question']}\nA: {item['answer']}" ...]
        documents = [f"Q: {q['question']}\nA: {q['answer']}" for q in new_questions]
        
        # Use simple batching
        batch_size = 64
        all_embeddings = []
        
        for i in tqdm(range(0, len(documents), batch_size), desc="Embedding"):
            batch = documents[i:i+batch_size]
            embeddings = self.model.encode(batch, convert_to_numpy=True, show_progress_bar=False)
            all_embeddings.append(embeddings)
        
        if not all_embeddings:
            return

        # Combine
        embeddings_array = np.vstack(all_embeddings).astype('float32')
        
        # Normalize
        faiss.normalize_L2(embeddings_array)
        
        print(f"✅ Generated {len(embeddings_array)} embeddings")
        
        # Add to FAISS
        print(f"\n📥 Adding to FAISS index...")
        index.add(embeddings_array)
        
        # Add to metadata
        # Ensure 'language' field is present
        for q in new_questions:
            q['language'] = language
            
        metadata.extend(new_questions)
        
        print(f"✅ Index now has {index.ntotal} documents")
        
        # Save back
        if language == "English":
            self.english_index = index
            self.english_metadata = metadata
        else:
            self.urdu_index = index
            self.urdu_metadata = metadata
    
    def save_indices(self):
        """Save updated indices and metadata"""
        print(f"\n{'='*80}")
        print("💾 Saving updated indices...")
        print(f"{'='*80}")
        
        # English
        if self.english_index:
            en_index_path = os.path.join(self.index_dir, "english.index")
            en_meta_path = os.path.join(self.index_dir, "english_metadata.pkl")
            try:
                faiss.write_index(self.english_index, en_index_path)
                with open(en_meta_path, 'wb') as f:
                    pickle.dump(self.english_metadata, f)
                print(f"✅ Saved English index: {self.english_index.ntotal} documents")
            except Exception as e:
                print(f"❌ Error saving English index: {e}")

        # Urdu
        if self.urdu_index:
            ur_index_path = os.path.join(self.index_dir, "urdu.index")
            ur_meta_path = os.path.join(self.index_dir, "urdu_metadata.pkl")
            try:
                faiss.write_index(self.urdu_index, ur_index_path)
                with open(ur_meta_path, 'wb') as f:
                    pickle.dump(self.urdu_metadata, f)
                print(f"✅ Saved Urdu index: {self.urdu_index.ntotal} documents")
            except Exception as e:
                print(f"❌ Error saving Urdu index: {e}")

    def update_index(self, file_path, language):
        """Convenience method to update a single language index"""
        if language == "English":
            meta = self.english_metadata
        else:
            meta = self.urdu_metadata
            
        new_qs = self.get_new_questions(file_path, meta)
        self.add_to_index(new_qs, language)
        self.save_indices()

if __name__ == "__main__":
    print("\n" + "="*80)
    print("🚀 INCREMENTAL FAISS INDEXING")
    print("="*80)
    
    indexer = IncrementalIndexer()
    
    # Load existing indices
    if not indexer.load_existing_indices():
        print("\n❌ ERROR: Could not load any indices!")
        # If no indices, we might want to CREATE them? 
        # But this is incremental. The user should have base indices.
        print("Please ensure 'backend/vector_db_faiss' has valid indices.")
    
    # Paths (Defaulting to the production datasets)
    FILE_EN = "dataset/TB_QA_DATASET_ENGLISH.json"
    FILE_UR = "dataset/TB_QA_DATASET_URDU_100K.json"
    
    if os.path.exists(FILE_EN):
        indexer.update_index(FILE_EN, "English")
        
    if os.path.exists(FILE_UR):
        indexer.update_index(FILE_UR, "Urdu")
