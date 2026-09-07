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

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]

@app.get("/")
def health_check():
    return {"status": "Vesper.ai Conversational Engine Online"}

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        system_instruction = {
            "role": "system",
            "content": "You are Vesper.ai, a sharp, ultra-capable AI assistant and autonomous agent. Keep responses clear, helpful, and concise."
        }
        
        full_messages = [system_instruction] + [msg.model_dump() for msg in request.messages]

        # Updated to official Groq model ID
        completion = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=full_messages,
            temperature=0.7,
            max_tokens=1024
        )

        assistant_reply = completion.choices[0].message.content

        return {
            "success": True,
            "reply": assistant_reply
        }
    except Exception as e:
        print(f"Error executing chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))
