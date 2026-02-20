from fastapi import FastAPI, Query, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import sqlite3
import os
import shutil
import time
from typing import List, Optional
from pydantic import BaseModel

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# RAG System Import
try:
    from rag_engine import RAGEngine
    RAG_AVAILABLE = True
except Exception as e:
    RAG_AVAILABLE = False
    print(f"⚠️  RAG Engine not available: {e}")

# X-Ray System Import
try:
    from xray_classifier import XRayClassifier
    XRAY_AVAILABLE = True
except Exception as e:
    XRAY_AVAILABLE = False
    print(f"⚠️  X-Ray Classifier not available: {e}")


app = FastAPI(title="TB Expert Search API", version="1.0.0")

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Resolve relative path correctly regardless of execution dir
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'tb_expert.db')

# Conversation memory storage (session-based)
# In production, use Redis or database. For now, in-memory dict
conversation_history = {}  # {session_id: [messages]}

# Initialize RAG Engine (if available)
rag_engine = None
if RAG_AVAILABLE:
    try:
        from rag_engine import RAGEngine
        gemini_key = os.getenv("GEMINI_API_KEY")  # Optional: set in environment
        rag_engine = RAGEngine(gemini_api_key=gemini_key)
        print("✅ RAG Engine initialized and ready")
    except Exception as e:
        print(f"⚠️  RAG Engine initialization failed: {e}")
        rag_engine = None

# Initialize X-Ray Classifier (if available)
xray_classifier = None
if XRAY_AVAILABLE:
    try:
        model_path = os.path.join(BASE_DIR, 'models', 'xray_tb_model')
        xray_classifier = XRayClassifier(model_path)
    except Exception as e:
        print(f"⚠️  X-Ray initialization failed: {e}")

# Ensure upload directory exists
UPLOAD_DIR = os.path.join(BASE_DIR, 'static', 'uploads')
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Mount static files for images
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, 'static')), name="static")

def get_conversation_context(session_id: str, max_messages: int = 5) -> List[str]:
    """Get last N messages from conversation history"""
    if session_id not in conversation_history:
        conversation_history[session_id] = []
    return conversation_history[session_id][-max_messages:]

def add_to_conversation(session_id: str, message: str):
    """Add message to conversation history"""
    if session_id not in conversation_history:
        conversation_history[session_id] = []
    conversation_history[session_id].append(message)
    # Keep only last 10 messages to avoid memory issues
    if len(conversation_history[session_id]) > 10:
        conversation_history[session_id] = conversation_history[session_id][-10:]


class QAResponse(BaseModel):
    id: str
    language: str
    category: str
    question: str
    answer: str
    score: float

@app.get("/")
def home():
    return {"status": "online", "message": "TB Expert Search API is running"}

@app.get("/search", response_model=List[QAResponse])
def search(q: str = Query(..., min_length=2), lang: Optional[str] = None, limit: int = 10):
    """
    Lightning-fast bilingual search across 200,000 records.
    Cleaned for natural language inputs.
    """
    if not os.path.exists(DB_PATH):
        return []

    # Clean query: Remove special characters often found in natural language
    import re
    clean_q = re.sub(r'[^\w\s]', ' ', q).strip()
    
    # If query is short, use prefix matching. If long, use phrase or standard tokens.
    words = clean_q.split()
    if len(words) == 1:
        fts_query = f"{words[0]}*"
    else:
        # For multiple words, we want them all to appear (AND logic)
        fts_query = " AND ".join(words)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Base SQL with BM25-like ranking
    query_sql = "SELECT id, language, category, question, answer, rank FROM qa_index WHERE qa_index MATCH ?"
    params = [fts_query]

    if lang:
        query_sql += " AND language = ?"
        params.append(lang.capitalize())

    query_sql += " ORDER BY rank LIMIT ?"
    params.append(limit)

    try:
        cursor.execute(query_sql, params)
        rows = cursor.fetchall()
    except sqlite3.OperationalError:
        # Fallback if FTS5 syntax fails
        cursor.execute("SELECT id, language, category, question, answer, -1.0 as rank FROM qa_index WHERE question LIKE ? LIMIT ?", (f"%{clean_q}%", limit))
        rows = cursor.fetchall()
        
    conn.close()

    results = []
    for row in rows:
        results.append({
            "id": row["id"],
            "language": row["language"],
            "category": row["category"],
            "question": row["question"],
            "answer": row["answer"],
            "score": abs(row["rank"]) # FTS5 rank is better when lower, so we show absolute
        })
    
    return results

class ChatRequest(BaseModel):
    message: str
    language: Optional[str] = None
    session_id: Optional[str] = "default"  # Session ID for conversation tracking

@app.post("/chat")
def chat(request: ChatRequest):
    """
    Unified RAG-Powered Chat Endpoint
    Uses semantic search + conversation context for intelligent responses
    """
    if not rag_engine:
        return {
            "reply": "System initializing... please wait.",
            "category": "System",
            "language": "English"
        }

    q = request.message
    is_urdu_query = any("\u0600" <= c <= "\u06FF" for c in q)
    detected_lang = "Urdu" if is_urdu_query else "English"
    
    # Override if specific language requested
    if request.language:
        detected_lang = request.language
    
    session_id = request.session_id or "default"
    
    # 1. Get Conversation History
    conversation_context = get_conversation_context(session_id, max_messages=5)
    
    # 2. RAG Processing
    try:
        # Enhance query with context
        enhanced_query = rag_engine.enhance_query_with_context(q, conversation_context, detected_lang)
        
        # Generate Answer with conversation history for symptom tracking
        result = rag_engine.generate_answer(
            enhanced_query, 
            language=detected_lang, 
            original_query=q,
            conversation_history=conversation_context
        )
        
        # 3. Store History
        add_to_conversation(session_id, f"Q: {q}")
        add_to_conversation(session_id, f"A: {result['answer'][:200]}")
        
        return {
            "reply": result['answer'],
            "category": result.get('category', 'General'),
            "language": detected_lang,
            "sources": result.get('sources', [])
        }
        
    except Exception as e:
        print(f"❌ Chat Error: {e}")
        return {
            "reply": "I encountered an error processing your request." if not is_urdu_query else "آپ کی درخواست پر عمل کرتے ہوئے مجھے ایک خرابی کا سامنا کرنا پڑا۔",
            "category": "Error",
            "language": detected_lang
        }

@app.get("/stats")
def get_stats():
    if not os.path.exists(DB_PATH):
        return {"error": "Index not built"}
        
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT language, count(*) FROM qa_index GROUP BY language")
    counts = dict(cursor.fetchall())
    
    cursor.execute("SELECT count(DISTINCT category) FROM qa_index")
    categories = cursor.fetchone()[0]
    
    conn.close()
    
    return {
        "total_records": sum(counts.values()),
        "breakdown": counts,
        "unique_categories": categories,
        "index_size_mb": os.path.getsize(DB_PATH) / (1024*1024)
    }

@app.post("/chat-rag")
def chat_rag(request: ChatRequest):
    """
    RAG-Powered Chat Endpoint with Conversation Memory
    Uses semantic search + AI generation + conversation context for intelligent responses
    """
    if not rag_engine:
        return {
            "reply": "RAG system is not available. Please use /chat endpoint.",
            "category": "System",
            "method": "error"
        }
    
    q = request.message.strip()
    session_id = request.session_id or "default"
    
    # Get conversation history
    conversation_context = get_conversation_context(session_id, max_messages=5)
    
    # Detect language
    is_urdu_query = any("\u0600" <= c <= "\u06FF" for c in q)
    detected_lang = "Urdu" if is_urdu_query else "English"
    
    # Override if user specifies
    if request.language:
        detected_lang = request.language
    
    try:
        # Enhance query with conversation context
        enhanced_query = rag_engine.enhance_query_with_context(q, conversation_context, detected_lang)
        
        # Use RAG engine to generate answer with conversation history
        result = rag_engine.generate_answer(
            enhanced_query, 
            language=detected_lang, 
            original_query=q,
            conversation_history=conversation_context
        )
        
        # Add to conversation history
        add_to_conversation(session_id, f"Q: {q}")
        add_to_conversation(session_id, f"A: {result['answer'][:200]}")  # Store first 200 chars
        
        # Format response
        response = {
            "reply": result['answer'],
            "method": result['method'],
            "language": detected_lang,
            "session_id": session_id
        }
        
        # Add category if available
        if 'category' in result:
            response['category'] = result['category']
        
        # Add sources if available
        if result.get('sources'):
            response['sources'] = [
                {
                    "category": src['category'],
                    "question": src['question'][:100],
                    "relevance": round(src['relevance_score'], 3)
                }
                for src in result['sources'][:3]
            ]
        
        return response
        
    except Exception as e:
        print(f"❌ RAG Error: {e}")
        import traceback
        traceback.print_exc()
        return {
            "reply": f"An error occurred: {str(e)}",
            "category": "Error",
            "method": "error"
        }

class XRayResponse(BaseModel):
    prediction: str
    confidence: float
    image_url: str
    message: str

@app.post("/predict-xray", response_model=XRayResponse)
async def predict_xray(file: UploadFile = File(...)):
    """
    Handle X-ray image upload and return prediction
    """
    if not xray_classifier:
        return XRayResponse(
            prediction="Error",
            confidence=0.0,
            image_url="",
            message="X-Ray model not initialized correctly."
        )

    try:
        # Save the uploaded file
        timestamp = int(time.time())
        filename = f"{timestamp}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIR, filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Performance prediction
        prediction, confidence = xray_classifier.predict(file_path)
        
        # Build image URL (assuming backend runs on port 8000)
        # In production, this should be relative or from config
        image_url = f"/static/uploads/{filename}"
        
        message = "AI Scan Results: Tuberculosis Detected" if prediction == "Tuberculosis" else "AI Scan Results: Normal (No TB Detected)"
        
        return XRayResponse(
            prediction=prediction,
            confidence=round(confidence, 4),
            image_url=image_url,
            message=message
        )
        
    except Exception as e:
        print(f"❌ X-Ray Prediction Error: {e}")
        return XRayResponse(
            prediction="Error",
            confidence=0.0,
            image_url="",
            message=f"Processing failed: {str(e)}"
        )


# SPA Routing - Catch-all to serve index.html for frontend sub-routes
@app.get("/{rest_of_path:path}")
async def serve_frontend(rest_of_path: str):
    # Exclude API and static paths from being caught as SPA routes
    if rest_of_path.startswith("api/") or rest_of_path.startswith("static/"):
        return {"detail": "Not Found"}
        
    # If it looks like a file (has an extension), return not found
    if "." in rest_of_path.split("/")[-1]:
         return {"detail": "Not Found"}

    frontend_index = os.path.join(BASE_DIR, 'static', 'dist', 'index.html')
    if os.path.exists(frontend_index):
        return FileResponse(frontend_index)
    
    return {"status": "backend_only", "message": "Frontend build not found."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
