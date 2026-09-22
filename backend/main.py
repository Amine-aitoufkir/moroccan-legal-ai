"""Point d'entree de l'API Moroccan Legal AI."""

from fastapi import FastAPI

app = FastAPI(title="Moroccan Legal AI API")


@app.get("/health")
def health() -> dict[str, str]:
    """Indique si le processus API repond aux requetes."""
    return {"status": "ok"}
