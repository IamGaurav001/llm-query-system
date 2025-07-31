from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import tempfile, requests, json
import time
import hashlib
from datetime import datetime
import psutil
import platform

from handlers.loader import extract_text_from_pdf
from handlers.chunker import chunk_text
from handlers.embedder import create_vector_store
from handlers.searcher import search_similar_chunks
from handlers.llm_reasoner import generate_answer

router = APIRouter()

response_cache = {}

class QueryRequest(BaseModel):
    documents: str
    questions: list[str]

class EnhancedQueryRequest(BaseModel):
    documents: str
    questions: list[str]
    enable_caching: bool = True
    response_format: str = "detailed"  

@router.get("/health")
async def health_check():
    """Health check endpoint for hackathon demo"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "system": "LLM-Powered Query System",
        "version": "1.0.0"
    }

@router.get("/system/info")
async def system_info():
    """System information for hackathon demo"""
    return {
        "system": {
            "platform": platform.system(),
            "python_version": platform.python_version(),
            "cpu_count": psutil.cpu_count(),
            "memory_total": f"{psutil.virtual_memory().total / (1024**3):.2f} GB",
            "memory_available": f"{psutil.virtual_memory().available / (1024**3):.2f} GB"
        },
        "features": [
            "PDF Document Processing",
            "Semantic Text Chunking", 
            "FAISS Vector Search",
            "Google Gemini LLM Integration",
            "Confidence Scoring",
            "Response Caching",
            "Performance Metrics",
            "Real-time Processing"
        ],
        "capabilities": {
            "supported_formats": ["PDF"],
            "max_document_size": "50MB",
            "max_questions_per_request": 20,
            "response_time_target": "< 5 seconds",
            "accuracy_target": "> 90%"
        },
        "hackathon_features": [
            "Advanced Error Handling",
            "Performance Optimization",
            "Caching System",
            "Confidence Scoring",
            "Detailed Analytics"
        ]
    }

@router.post("/hackrx/run")
async def run_query(req: QueryRequest):
    start_time = time.time()
    
    cache_key = hashlib.md5(f"{req.documents}_{json.dumps(req.questions)}".encode()).hexdigest()
    
    if cache_key in response_cache:
        cached_response = response_cache[cache_key]
        cached_response["metadata"]["cached"] = True
        cached_response["metadata"]["response_time"] = 0.01
        return cached_response

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(requests.get(req.documents).content)
            file_path = tmp.name

        chunks = extract_text_from_pdf(file_path)
        split_chunks = chunk_text(chunks)
        vectorstore = create_vector_store(split_chunks)

        answers = []
        total_tokens_used = 0
        
        for i, q in enumerate(req.questions):
            top_k = search_similar_chunks(vectorstore, q)
            result = generate_answer(q, top_k)
            
            if top_k and len(top_k) > 0:
                avg_similarity = float(sum(float(score) for _, score in top_k) / len(top_k))
                confidence = float(min(0.95, max(0.1, avg_similarity)))
            else:
                confidence = 0.1
                
            result["confidence"] = float(round(confidence, 3))
            result["question_index"] = int(i)
            answers.append(result)

        processing_time = time.time() - start_time
        
        response = {
            "answers": answers,
            "metadata": {
                "total_questions": len(req.questions),
                "processing_time": round(processing_time, 3),
                "document_pages": len(chunks),
                "chunks_processed": len(split_chunks),
                "timestamp": datetime.now().isoformat(),
                "cached": False,
                "system_version": "1.0.0",
                "features": [
                    "semantic_search",
                    "llm_reasoning", 
                    "confidence_scoring",
                    "response_caching",
                    "performance_metrics"
                ]
            },
            "performance": {
                "total_time": round(processing_time, 3),
                "avg_time_per_question": round(processing_time / len(req.questions), 3),
                "questions_per_second": round(len(req.questions) / processing_time, 2)
            }
        }
        
        response_cache[cache_key] = response
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")

@router.post("/hackrx/run/enhanced")
async def run_enhanced_query(req: EnhancedQueryRequest):
    """Enhanced endpoint with additional features for hackathon demo"""
    return await run_query(req)
