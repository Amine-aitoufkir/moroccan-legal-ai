# Controle qualite - Frontend

## Verification effectuee

Avant de creer le premier commit Git, le frontend a ete controle avec :

~~~powershell
cd frontend
npm run lint
~~~

Le resultat ne contenait aucune erreur. Le controle a donc reussi.

## Difference entre les deux commandes importantes

~~~text
npm run dev   = lance le site en developpement et reste actif
npm run lint  = analyse le code, puis se termine
~~~

La commande npm run dev demarre Next.js. Elle affiche une adresse locale, souvent http://localhost:3000, et le navigateur peut afficher le site. Elle reste active jusqu'a Ctrl + C.

La commande npm run lint ne lance aucun site. Elle utilise ESLint pour chercher des erreurs et des mauvaises pratiques dans le code. Elle est normalement lancee avant un commit ou avant d'envoyer son travail a un collegue.
