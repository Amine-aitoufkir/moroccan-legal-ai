"""Point d'entree de l'API Moroccan Legal AI."""

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="Moroccan Legal AI API")


class ChatRequest(BaseModel):
    """Donnees envoyees par le frontend pour poser une question."""

    question: str = Field(min_length=3, max_length=2000)


class ChatResponse(BaseModel):
    """Format stable de la reponse renvoyee au frontend."""

    answer: str
    sources: list[str]


@app.get("/health")
def health() -> dict[str, str]:
    """Indique si le processus API repond aux requetes."""
    return {"status": "ok"}


@app.post("/api/v1/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    """Valide une question avant le futur traitement juridique."""
    return ChatResponse(
        answer=(
            "Question reçue. Le moteur juridique et le RAG ne sont pas "
            "encore connectés, donc aucune réponse juridique n'est générée."
        ),
        sources=[],
    )
