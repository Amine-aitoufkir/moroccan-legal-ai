# Moroccan Legal AI

Projet portfolio en monorepo : interface Next.js et API FastAPI. Supabase, recherche documentaire juridique et agents seront ajoutes par etapes.

## Structure actuelle

~~~text
frontend/  Interface Next.js
backend/   API FastAPI et tests
docs/      Notes d'installation et explications
~~~

## Demarrage local

Dans un terminal, lancer le frontend :

~~~powershell
cd frontend
npm install
npm run dev
~~~

Dans un autre terminal, lancer le backend :

~~~powershell
cd backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn main:app --reload
~~~

Ces commandes de creation et d'installation sont necessaires seulement lors de la premiere installation. Aux lancements suivants, activer .venv et executer la derniere commande.

Ouvrir http://127.0.0.1:8000/health pour verifier l'API. La documentation interactive est disponible sur http://127.0.0.1:8000/docs.

Le premier contrat de chat est disponible avec POST http://127.0.0.1:8000/api/v1/chat. Il valide une question mais renvoie encore une reponse de demonstration, sans conseil juridique ni RAG.

Ouvrir http://localhost:3000 pour voir dans le frontend si l'API repond. Le frontend utilise l'adresse http://127.0.0.1:8000 par defaut. Pour une autre adresse, copier frontend/.env.example vers frontend/.env.local et modifier BACKEND_URL. Ce fichier local est ignore par Git.

Pour lancer les tests du backend depuis backend/ :

~~~powershell
python -m unittest discover -s tests -v
~~~

Voir [l'installation expliquee](docs/installation-locale.md) pour comprendre chaque commande.
