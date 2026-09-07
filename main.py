import os
import re
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv

# Load environment variables (locally or from Render env)
load_dotenv()

app = FastAPI(title="Vesper AI Hybrid Text/Vision Engine")

# Configure CORS for mobile/web app access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Groq client with error handling
groq_api_key = os.getenv("GROQ_API_KEY")
groq_client = None
if groq_api_key:
    groq_client = Groq(api_key=groq_api_key)
else:
    print("WARNING: GROQ_API_KEY is not set.")

@app.get("/")
def health_check():
    return {"status": "Vesper Engine Online", "groq_connected": bool(groq_client)}

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]

# Endpoint 1: Normal Vesper Chat
@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    if not groq_client:
        raise HTTPException(status_code=500, detail="GROQ client not initialized.")

    try:
        system_instruction = {
            "role": "system",
            "content": (
                "You are Vesper.ai, a slick AI assistant built for local business owners."
                "CRITICAL: Never use Markdown tables or columns. Format everything with clean bullet points and short paragraphs."
                "If the user asks for design help, give sharp, creative advice."
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

class PromptRequest(BaseModel):
    user_prompt: str

# Endpoint 2: Advanced Image Prompt Expansion (THE FIX)
@app.post("/api/expand_image_prompt")
async def expand_image_prompt(request: PromptRequest):
    if not groq_client:
        raise HTTPException(status_code=500, detail="GROQ client not initialized.")

    try:
        expansion_instruction = [
            {"role": "system", "content": (
                "You are an expert AI art director specializing in photorealism."
                "Your task is to take a short, simple user request and automatically rewrite it into a hyper-detailed, professional image generation prompt."
                "Add details like camera type (e.g., Canon EOS R5), lens (e.g., 50mm f/1.8), specific lighting (e.g., cinematic, soft morning light, volumetric fog), texture (e.g., white marble, polished concrete), and resolution (e.g., 8k, photorealistic, Unreal Engine 5 render)."
                "Output ONLY the new expanded text prompt. Do not add any preamble or meta-commentary."
            )},
            {"role": "user", "content": f"User: {request.user_prompt}"}
        ]

        completion = groq_client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=expansion_instruction,
            temperature=0.8, # Slightly higher for more creative expansion
            max_tokens=200 # Keep the prompt reasonable
        )

        expanded_text = completion.choices[0].message.content.strip()
        
        # Security/Sanity check: Ensure no preamble slipped in
        clean_prompt = re.sub(r"^(Here is the expanded prompt:|Here is your detailed prompt:)\s*", "", expanded_text, flags=re.IGNORECASE)

        return {
            "success": True,
            "expanded_prompt": clean_prompt
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
