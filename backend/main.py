"""Point d'entree de l'API Moroccan Legal AI."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from supabase_client import check_supabase_connection

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


@app.get("/health/supabase")
def supabase_health() -> dict[str, str]:
    """Indique si FastAPI peut joindre Supabase sans exposer de secret."""
    try:
        check_supabase_connection()
    except Exception as error:
        raise HTTPException(
            status_code=503,
            detail="La connexion Supabase est indisponible.",
        ) from error

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
