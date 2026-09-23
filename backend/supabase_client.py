"""Client Supabase reserve au backend FastAPI."""

import os
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from supabase import Client, create_client


# Le chemin explicite permet de trouver backend/.env, meme si FastAPI est lance
# depuis la racine du monorepo.
load_dotenv(Path(__file__).with_name(".env"))


@lru_cache
def get_supabase_client() -> Client:
    """Construit une seule connexion Supabase reutilisee par le backend."""
    url = os.getenv("SUPABASE_URL")
    secret_key = os.getenv("SUPABASE_SECRET_KEY")

    if not url or not secret_key:
        raise RuntimeError(
            "SUPABASE_URL et SUPABASE_SECRET_KEY doivent etre definies dans backend/.env."
        )

    return create_client(url, secret_key)


def check_supabase_connection() -> None:
    """Verifie que le backend peut lire la table conversations."""
    get_supabase_client().table("conversations").select("id").limit(1).execute()
