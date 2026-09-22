# Installation locale - Moroccan Legal AI

Ce document explique simplement ce que nous avons fait pour preparer le projet sur Windows. Quand tu reviens sur le projet, lis d'abord la section « Reprendre le travail ».

## 1. L'idee generale

Notre projet est une application composee de deux parties :

~~~text
frontend/  = ce que l'utilisateur voit dans son navigateur
backend/   = le cerveau qui traite les demandes
~~~

Plus tard, le backend parlera avec Supabase, les documents juridiques et les outils d'IA.

## 2. Le frontend Next.js

Au debut, le frontend a ete cree avec :

~~~powershell
npx create-next-app@latest frontend
~~~

Cette commande est utilisee une seule fois : elle cree tout le projet frontend.

Explication simple :

- npx : lance un outil Node.js sans l'installer pour toujours sur le PC ;
- create-next-app : outil officiel qui construit un nouveau projet Next.js ;
- @latest : demande la version la plus recente ;
- frontend : nom du dossier que l'outil cree.

Le resultat est un dossier frontend contenant notamment :

~~~text
frontend/
├── app/           # pages et interface du site
├── public/        # images et fichiers publics
├── package.json   # liste des outils JavaScript utilises
└── node_modules/  # outils telecharges par npm, a ne pas modifier
~~~

Dans ce projet, le dossier app/ est directement dans frontend/. Le dossier src/ est facultatif : son absence est normale.

Pour lancer le frontend apres sa creation :

~~~powershell
cd frontend
npm run dev
~~~

Le terminal affiche une adresse, souvent http://localhost:3000. Il faut l'ouvrir dans le navigateur. Pour arreter le serveur, utiliser Ctrl + C.

## 3. Le dossier backend

Nous avons cree le dossier backend avec :

~~~powershell
mkdir backend
~~~

Important : cette commande a cree seulement un dossier vide appele backend. Elle n'a pas cree Python, FastAPI, Lib ou Scripts.

~~~text
moroccan-legal-ai/
├── frontend/
└── backend/       # vide juste apres mkdir backend
~~~

## 4. Python est deja installe

Nous avons verifie Python avec :

~~~powershell
cd backend
py --version
~~~

Resultat obtenu :

~~~text
Python 3.14.4
~~~

Donc Python etait deja installe une seule fois sur Windows. Nous ne l'avons pas reinstalle pour ce projet.

## 5. L'environnement virtuel .venv

Nous avons ensuite execute :

~~~powershell
py -m venv .venv
~~~

Pense a .venv comme une boite privee pour ce projet. Elle permet d'installer les bibliotheques du backend sans melanger les bibliotheques des autres projets Python.

Cette commande a cree automatiquement :

~~~text
backend/
└── .venv/
    ├── Include/       # fichiers techniques : ne pas toucher
    ├── Lib/           # bibliotheques Python de ce projet
    │   └── site-packages/  # FastAPI est installe ici
    ├── Scripts/       # commandes pour Windows
    │   ├── python.exe
    │   ├── pip.exe
    │   └── Activate.ps1
    ├── .gitignore
    └── pyvenv.cfg
~~~

En resume :

~~~text
mkdir backend            -> cree seulement backend/
py -m venv .venv         -> cree .venv/ et son contenu automatique
pip install ...           -> ajoute les bibliotheques dans .venv/Lib/site-packages/
~~~

.venv prend un peu de place, mais c'est normal. Il ne faut jamais l'envoyer sur Git, car il est possible de le recreer plus tard.

## 6. Activer .venv

Nous avons active l'environnement avec :

~~~powershell
.\.venv\Scripts\Activate.ps1
~~~

Quand le terminal commence par (.venv), cela veut dire : « les commandes Python de ce terminal utilisent maintenant le Python prive de ce projet ».

~~~text
(.venv) PS C:\...\backend>
~~~

La difference importante est :

- py -m venv .venv : cree .venv une seule fois ;
- Activate.ps1 : active .venv dans le terminal ouvert maintenant.

Si tu fermes le terminal, .venv existe toujours, mais elle n'est plus active. Il faut donc l'activer de nouveau la prochaine fois. Pour sortir volontairement :

~~~powershell
deactivate
~~~

## 7. pip et FastAPI

pip est l'outil qui telecharge et installe des bibliotheques Python. Il ressemble a npm dans un projet Next.js.

Nous avons mis pip a jour :

~~~powershell
python -m pip install --upgrade pip
~~~

Cette commande met a jour seulement pip dans .venv. Elle ne reinstalle pas Python et n'installe pas encore FastAPI.

Ensuite, nous avons installe FastAPI :

~~~powershell
python -m pip install "fastapi[standard]"
~~~

FastAPI est l'outil qui nous permet de creer une API backend. Sans FastAPI, nous ne pouvons pas creer les routes qui recoivent les demandes du frontend.

Exemples de routes que nous creerons plus tard :

~~~text
GET  /health          = verifier que le backend fonctionne
POST /api/chat        = recevoir une question de l'utilisateur
POST /api/documents   = ajouter un document au RAG
~~~

FastAPI a ete ajoute dans .venv/Lib/site-packages/. La commande fastapi.exe a aussi ete ajoutee dans .venv/Scripts/.

Pour verifier que FastAPI est installe :

~~~powershell
python -m pip show fastapi
~~~

## 8. Reprendre le travail un autre jour

### Pour travailler sur le frontend

~~~powershell
cd frontend
npm run dev
~~~

### Pour travailler sur le backend

~~~powershell
cd backend
.\.venv\Scripts\Activate.ps1
~~~

Apres l'activation, le prefixe (.venv) doit apparaitre. Le serveur FastAPI n'est pas encore cree : la prochaine etape sera de creer le fichier main.py et une route /health.

## 9. Protection Git avec .gitignore

Un fichier .gitignore a ete cree a la racine du projet. Il indique a Git les fichiers qui ne doivent jamais etre enregistres dans le depot.

Il protege notamment :

~~~text
frontend/node_modules/  = dependances JavaScript telechargees
frontend/.next/         = fichiers generes par Next.js
backend/.venv/          = environnement Python local
.env                    = futures cles et mots de passe
~~~

Ce fichier ne supprime aucun fichier du PC. Il dit seulement a Git de ne pas les ajouter dans un commit.

Verification executee :

~~~powershell
git check-ignore -v backend/.venv/Scripts/python.exe
~~~

Le resultat a montre que la regle backend/.venv/ du .gitignore racine ignore correctement l'environnement Python.

## Regle a retenir

Nous ajouterons une explication dans ce document apres chaque etape importante. Ne jamais copier une commande sans savoir dans quel dossier elle doit etre lancee et ce qu'elle va changer.
