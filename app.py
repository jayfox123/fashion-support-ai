from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from agents.supervisor import handle_customer_message
from utils.voice_service import text_to_speech
from config import settings
import io

app = FastAPI(title="Fashion Support AI", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Fashion Support AI is running", "status": "healthy"}

@app.post("/api/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        message = data.get("message", "")
        context = data.get("context", {})

        if not message:
            return JSONResponse(
                status_code=400,
                content={"error": "Message cannot be empty"}
            )

        result = handle_customer_message(message, context)

        return JSONResponse(content={
            "response": result["response"],
            "agent_used": result["agent_used"],
            "status": "success"
        })

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "status": "error"}
        )

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "agents": [
            "order_agent",
            "query_agent",
            "recommendation_agent",
            "returns_agent",
            "escalation_agent"
        ]
    }

@app.post("/api/voice")
async def voice(request: Request):
    try:
        data = await request.json()
        text = data.get("text", "")

        if not text:
            return JSONResponse(
                status_code=400,
                content={"error": "Text cannot be empty"}
            )

        audio = text_to_speech(text)
        return StreamingResponse(io.BytesIO(audio), media_type="audio/mpeg")

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "status": "error"}
        )