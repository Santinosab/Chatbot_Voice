# backend/main.py

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from transformers import pipeline, Conversation

app = FastAPI()

# Opción 1: permitir todos los orígenes SIN credenciales
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # permite cualquier origen
    allow_credentials=False,       # NO enviamos ni aceptamos cookies/autorizaciones
    allow_methods=["*"],           # permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],           # permite todas las cabeceras
)

# Carga el modelo de chat
chatbot = pipeline("conversational", model="facebook/blenderbot-400M-distill")

@app.post("/chat")
async def chat(request: Request):
    body = await request.json()
    user_input = body.get("message", "")
    conversation = Conversation(user_input)
    response = chatbot(conversation)
    return {"response": response.generated_responses[-1]}

# Para ejecutar:
# uvicorn backend.main:app --reload
