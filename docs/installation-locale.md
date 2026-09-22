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

FastAPI est l'outil choisi pour creer notre API backend. Python peut aussi creer des API avec d'autres outils ; FastAPI facilite les routes qui recoivent les demandes du frontend.

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

Apres l'activation, le prefixe (.venv) doit apparaitre. Le serveur FastAPI peut maintenant etre lance avec python -m uvicorn main:app --reload depuis backend/.

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

## 10. Premiere API FastAPI

Le fichier backend/main.py contient l'objet app = FastAPI(...). Cet objet est l'application web du backend. La fonction health est associee a GET /health : lorsque le navigateur ouvre cette adresse, l'API renvoie {"status": "ok"}.

Le fichier backend/requirements.txt liste FastAPI avec la version utilisee pour ce projet. Un nouveau developpeur peut ainsi recreer son environnement avec :

~~~powershell
cd backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
~~~

La premiere commande cree l'environnement. On ne la repete pas si .venv existe deja. La deuxieme l'active dans le terminal actuel. La derniere installe les bibliotheques listees dans requirements.txt.

Pour lancer l'API depuis backend/ :

~~~powershell
python -m uvicorn main:app --reload
~~~

- python -m uvicorn lance le serveur web installe avec FastAPI ;
- main:app signifie « trouve l'objet app dans le fichier main.py » ;
- --reload redemarre automatiquement le serveur quand le code change. A utiliser seulement en developpement.

Ensuite, ouvrir http://127.0.0.1:8000/health. La reponse attendue est {"status": "ok"}. La page http://127.0.0.1:8000/docs presente la documentation interactive generee par FastAPI. Ctrl + C arrete le serveur.

Pour verifier automatiquement /health depuis backend/ :

~~~powershell
python -m unittest discover -s tests -v
~~~

Ce test envoie une requete a l'application et verifie le code HTTP 200 et la reponse JSON. Il utilise unittest, deja inclus avec Python.

## 11. Branche Git de cette etape

Le depot avait deux branches : main, qui contient seulement le commit initial du depot distant, et v1, qui contient le premier commit du frontend et de la documentation. La branche feat/backend-bootstrap a ete creee a partir de v1 pour developper le backend. Il faudra organiser ensuite l'integration de ces changements dans main ; rien n'est encore envoye sur GitHub.

## 12. Connexion du frontend au backend

La page frontend/app/page.tsx a ete remplacee par une page qui affiche l'etat de l'API. Elle appelle GET /health sur FastAPI et montre « API FastAPI connectee » quand la reponse est correcte.

La page est un composant serveur Next.js : l'appel a l'API part du serveur Next.js. Le navigateur recoit ensuite la page deja preparee. Cela evite pour cette premiere connexion un appel direct du navigateur a FastAPI et une configuration CORS.

La variable BACKEND_URL permet de changer l'adresse de l'API. Par defaut, elle vaut http://127.0.0.1:8000. Le fichier frontend/.env.example montre cette configuration sans contenir de secret. Si necessaire, copier ce fichier dans frontend/.env.local, modifier l'adresse et relancer Next.js. Le fichier .env.local reste sur le PC et n'est pas envoye sur Git.

Pour verifier la connexion, ouvrir deux terminaux :

~~~powershell
# Terminal 1, depuis backend/
.\.venv\Scripts\Activate.ps1
python -m uvicorn main:app --reload
~~~

~~~powershell
# Terminal 2, depuis frontend/
npm run dev
~~~

Ouvrir http://localhost:3000 : la page doit afficher que l'API est connectee. Si le backend est arrete, elle affiche qu'il est indisponible. Rafraichir la page apres avoir demarre ou arrete le backend.

Le template Next.js utilisait initialement les polices Google Geist. Le build devait les telecharger et echouait dans un environnement sans acces au site Google Fonts. Nous utilisons maintenant des polices systeme dans frontend/app/globals.css pour que le projet puisse etre construit hors ligne.

## 13. Premier contrat de chat

Le backend expose maintenant POST /api/v1/chat. Contrairement a GET /health, POST sert a envoyer des donnees. Le frontend envoie un objet JSON comme {"question": "Quels sont mes droits ?"}.

FastAPI utilise ChatRequest pour verifier que question contient entre 3 et 2000 caracteres. Une demande valide recoit un objet avec answer et sources. Une question trop courte recoit automatiquement le code HTTP 422. La reponse actuelle indique clairement que le RAG n'est pas encore connecte : elle ne donne aucun conseil juridique.

Le formulaire interactif se trouve dans frontend/app/components/chat-form.tsx. Il est marque use client parce qu'il gere la saisie, le clic et l'etat de chargement dans le navigateur.

Le navigateur appelle POST /api/chat dans Next.js. Le fichier frontend/app/api/chat/route.ts transmet ensuite la demande a FastAPI. Cette route intermediaire garde l'adresse interne du backend cote serveur et evitera d'exposer des secrets ou une configuration CORS au navigateur.

Le trajet complet est :

~~~text
Formulaire du navigateur
→ POST /api/chat sur Next.js
→ POST /api/v1/chat sur FastAPI
→ validation ChatRequest
→ reponse JSON ChatResponse
→ affichage dans le navigateur
~~~
