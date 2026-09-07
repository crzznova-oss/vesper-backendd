import os
from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq

app = FastAPI(title="Vesper.ai Chat Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"status": "Vesper.ai Conversational Engine Online"}

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="GROQ_API_KEY is missing in Render Environment Variables.")

    try:
        groq_client = Groq(api_key=api_key)
        
        system_instruction = {
            "role": "system",
            "content": (
                "You are Vesper.ai, a sharp AI assistant optimized for mobile UI. "
                "CRITICAL FORMATTING RULE: NEVER use Markdown tables or columns in your responses, as they break mobile screen layouts. "
                "Always format structured data, lists, features, or comparisons using clean bullet points (*), short paragraphs, and bold text headers."
            )
        }
        
        full_messages = [system_instruction] + [msg.model_dump() for msg in request.messages]

        completion = groq_client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=full_messages,
            temperature=0.7,
            max_tokens=1024
        )

        return {
            "success": True,
            "reply": completion.choices[0].message.content
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
