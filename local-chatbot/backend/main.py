# backend/main.py

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from transformers import pipeline, Conversation
import torch  # Import PyTorch to check for GPU availability

app = FastAPI()

# Opción 1: permitir todos los orígenes SIN credenciales
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # permite cualquier origen
    allow_credentials=False,       # NO enviamos ni aceptamos cookies/autorizaciones
    allow_methods=["*"],           # permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],           # permite todas las cabeceras
)

# Verifica si hay una GPU disponible
device = 0 if torch.cuda.is_available() else -1  # 0 for GPU, -1 for CPU

# Carga el modelo de chat en el dispositivo adecuado
chatbot = pipeline("conversational", model="facebook/blenderbot-3B", device=device)

@app.post("/chat")
async def chat(request: Request):
    body = await request.json()
    user_input = body.get("message", "")
    conversation = Conversation(user_input)
    response = chatbot(conversation)
    return {"response": response.generated_responses[-1]}

# Para ejecutar:
# uvicorn backend.main:app --reloads