import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq

app = FastAPI(title="Vesper.ai API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class WorkflowRequest(BaseModel):
    user_email: str
    workflow_description: str

@app.get("/")
def health_check():
    return {"status": "Vesper.ai Operational Engine Online"}

@app.post("/api/run-workflow")
async def run_workflow(request: WorkflowRequest):
    try:
        completion = groq_client.chat.completions.create(
            model="openai/gpt-oss-20b", 
            messages=[
                {
                    "role": "system",
                    "content": "You are Vesper.ai, an operational AI agent. Break down user workflows into step-by-step automated execution plans."
                },
                {
                    "role": "user",
                    "content": f"Automate this operational workflow: {request.workflow_description}"
                }
            ],
            temperature=0.2,
        )
        return {
            "success": True,
            "user": request.user_email,
            "execution_plan": completion.choices[0].message.content
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
