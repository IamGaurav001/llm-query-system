import os
from dotenv import load_dotenv
import google.generativeai as genai
import json

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_answer(query, top_chunks):
    context = "\n\n".join([f"(Page {c.metadata['page']}) {c.page_content}" for c, _ in top_chunks])

    prompt = f"""
You are an expert insurance policy analyst. Use this context to answer accurately.

Context:
{context}

Question:
{query}

Respond in JSON format:
{{
  "answer": "Your detailed answer here",
  "rationale": "Your reasoning for this answer",
  "source": {{
    "page": page_number,
    "text_snippet": "Relevant text from the document"
  }}
}}
"""
    
    try:
        model = genai.GenerativeModel("models/gemini-1.5-flash")  
        response = model.generate_content(prompt)
        
        if not response.text:
            return {
                "answer": "Unable to generate response",
                "rationale": "LLM returned empty response",
                "source": {"page": "unknown", "text_snippet": "No response generated"}
            }
        
        try:
            return json.loads(response.text.strip())
        except json.JSONDecodeError:
            return {
                "answer": response.text,
                "rationale": "LLM response could not be parsed as JSON",
                "source": {"page": "unknown", "text_snippet": "Response parsing error"}
            }
            
    except Exception as e:
        return {
            "answer": f"Error: {str(e)}",
            "rationale": "API call failed",
            "source": {"page": "unknown", "text_snippet": "Error occurred"}
        }
