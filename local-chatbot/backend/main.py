from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from transformers import pipeline, Conversation

app = FastAPI()

# CORS para permitir frontend React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cargar modelo
chatbot = pipeline("conversational", model="facebook/blenderbot-400M-distill")

@app.post("/chat")
async def chat(request: Request):
    body = await request.json()
    user_input = body.get("message", "")
    conversation = Conversation(user_input)
    response = chatbot(conversation)
    return {"response": response.generated_responses[-1]}
