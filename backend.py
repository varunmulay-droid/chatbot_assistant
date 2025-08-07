from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from models.mistral_openrouter import chat_with_mistral

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    try:
        reply = chat_with_mistral(request.message)
    except Exception as e:
        # Log the error (optional, but recommended for production)
        import logging
        logging.error(f"An error occurred: {e}")
        # Raise HTTPException with a 500 status code and a message
        raise HTTPException(status_code=500, detail="An error occurred while processing your request.")
    
    return {"response": reply}