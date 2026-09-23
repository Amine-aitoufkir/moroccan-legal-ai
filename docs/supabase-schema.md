# Schéma Supabase

Ce document décrit les tables créées dans le projet Supabase `moroccan-legal-ai-dev`.

## Table `conversations`

Une conversation représente une discussion complète entre un utilisateur et l'assistant. Les messages individuels seront ajoutés plus tard dans une table `messages` reliée à cette table.

| Colonne | Type | Rôle |
| --- | --- | --- |
| `id` | `uuid` | Identifiant unique de la conversation. Il est généré automatiquement par PostgreSQL. |
| `user_id` | `uuid` nullable | Utilisateur propriétaire de la conversation. Il référence `auth.users.id` de Supabase Auth. Il reste temporairement nullable tant que l'authentification n'est pas intégrée au frontend. |
| `title` | `text` | Titre de la conversation. La valeur par défaut est `Nouvelle conversation`. Un titre vide ou uniquement composé d'espaces est refusé. |
| `created_at` | `timestamptz` | Date et heure de création, automatiquement définie par `now()`. |
| `updated_at` | `timestamptz` | Date et heure de la dernière modification. Un déclencheur la met automatiquement à jour à chaque modification. |

## Sécurité

- RLS (Row Level Security) est activé sur `public.conversations`.
- Les utilisateurs non connectés (`anon`) ne peuvent rien lire ni modifier.
- Un utilisateur connecté peut uniquement lire, créer, modifier ou supprimer les lignes dont `user_id` correspond à son propre identifiant Supabase Auth.
- La fonction interne qui active automatiquement RLS sur les nouvelles tables n'est pas exécutable par les rôles publics `anon` et `authenticated`.

## Index

L'index `conversations_user_id_created_at_idx` accélère la recherche des conversations d'un utilisateur, triées par date de création.

## Table `messages`

Un message est un élément d'une conversation : une question de l'utilisateur, une réponse de l'assistant ou une instruction technique interne.

| Colonne | Type | Rôle |
| --- | --- | --- |
| `id` | `uuid` | Identifiant unique du message, généré automatiquement. |
| `conversation_id` | `uuid` | Conversation parente. Cette colonne référence `conversations.id` et elle est obligatoire. |
| `role` | `text` | Auteur logique du message : uniquement `user`, `assistant` ou `system`. |
| `content` | `text` | Contenu du message. Une valeur vide ou composée uniquement d'espaces est refusée. |
| `created_at` | `timestamptz` | Date et heure de création automatique. |

### Relation et suppression

`messages.conversation_id` est une clé étrangère vers `conversations.id` avec `ON DELETE CASCADE`. Lorsqu'une conversation est supprimée, PostgreSQL supprime automatiquement tous ses messages : il n'existe donc pas de messages orphelins.

### Accès aux messages

- RLS est activé sur `public.messages`.
- Un utilisateur connecté peut lire les messages des conversations dont il est propriétaire.
- Depuis le navigateur, il peut créer uniquement un message avec le rôle `user` dans sa propre conversation.
- Il n'existe volontairement pas de politique `UPDATE` ou `DELETE` sur les messages : l'historique est immuable. La suppression se fait en supprimant la conversation parente.
- Le backend FastAPI écrira plus tard les messages `assistant` et `system` côté serveur. Une clé secrète Supabase ne doit jamais être exposée au navigateur.

L'index `messages_conversation_id_created_at_idx` permet de charger rapidement les messages d'une conversation dans l'ordre chronologique.

## Historique des changements cloud

Les changements ont été appliqués via Supabase MCP le 22 septembre 2026 :

1. `create_conversations_table` : création de la table, de l'index et du déclencheur `updated_at`.
2. `secure_conversations_access` : politiques RLS et durcissement des permissions de la fonction automatique RLS.
3. `create_messages_table` : création de la table des messages, de sa relation, de son index et de ses politiques RLS.

## Prochaine étape

La prochaine étape est de connecter FastAPI à Supabase de façon sécurisée, sans exposer de clé secrète au frontend. Ensuite, l'API pourra enregistrer une conversation, le message de l'utilisateur et la réponse de l'assistant.

## Connexion backend

FastAPI est connecte a Supabase avec la cle secrete conservee dans `backend/.env`. Le role technique `service_role` dispose des droits `SELECT`, `INSERT`, `UPDATE` et `DELETE` sur `conversations` et `messages`. Cette cle ne doit jamais etre exposee au frontend.

Le changement cloud `grant_backend_table_access` a ete applique le 23 septembre 2026. La connexion reelle a ete verifiee par une lecture de la table `conversations` depuis le backend.

## Prochaine etape

La prochaine etape est Supabase Auth. L'utilisateur devra se connecter avant que FastAPI enregistre une conversation avec son `user_id`. Sans authentification, le backend ne doit pas enregistrer des discussions utilisateur car il ne peut pas attribuer correctement leur proprietaire.
