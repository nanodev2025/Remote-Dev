# Cursor Remote Dev — Telegram‑driven code & deploy agent

Bot Telegram open‑source qui te permet de piloter des modifications de code depuis ton mobile, puis de versionner (commit) et publier (push) automatiquement.

## Fonctionnalités
- **Télécommande via Telegram** : envoie une instruction en langage naturel.
- **Interpréteur IA** : transforme l’instruction en opérations de fichiers (create/modify/delete).
- **Git automatisé** : diff, reset, commit & push (si tout a réussi).
- **Feedback** : résumé + diff, et lien vers le commit si `GITHUB_REPO_URL` est fourni.
- **Sécurité** : verrouillage par `ALLOWED_USER_ID` + **PIN optionnel** (`ACCESS_PIN`).

## Structure
```
.
├── main.py                  # Point d'entrée du bot
├── requirements.txt         # Dépendances Python
├── src/
│   ├── bot.py              # Serveur Telegram bot
│   ├── ai_handler.py       # Gestion des API IA
│   └── git_manager.py      # Opérations Git automatisées
└── dot-env.example          # Template à copier en `.env`
```

## Prérequis
- Python **3.11+** (recommandé)
- Un dépôt Git (local) avec un remote `origin` si tu veux push
- Un bot Telegram (via `@BotFather`)

## Installation (bot)
```bash
git clone <ton-repo>
cd <ton-repo>

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Configuration
1) Copie le template :
```bash
cp dot-env.example .env
```

2) Édite `.env` et remplis :
- `TELEGRAM_TOKEN` : Token fourni par @BotFather
- `ALLOWED_USER_ID` : Ton ID Telegram (utilise @userinfobot)
- (recommandé) `ACCESS_PIN` : Code PIN optionnel pour sécurité renforcée
- `AI_PROVIDER` : Choisis un provider (`gemini`, `groq`, `openai`, `anthropic`, ou `ollama`)
- Clé API selon le provider :
  - `GEMINI_API_KEY` (gratuit via [Google AI Studio](https://aistudio.google.com/apikey))
  - `GROQ_API_KEY` (gratuit via [Groq Console](https://console.groq.com/keys))
  - `OPENAI_API_KEY` (payant)
  - `ANTHROPIC_API_KEY` (payant)
  - Aucune clé pour `ollama` (local)
- `GITHUB_REPO_URL` (optionnel mais utile pour les liens de commit)
- `WORKSPACE_PATH` (optionnel, par défaut `.`)

> `.env` est ignoré par Git via `.gitignore`. Ne le commit jamais.

## Démarrage
```bash
python main.py
```

## Commandes Telegram
- `/start` : onboarding
- `/help` : commandes
- `/id` : affiche ton user_id
- `/pin <code>` : déverrouille l’accès si `ACCESS_PIN` est défini
- `/status` : statut Git
- `/diff` : diff courant
- `/reset` : annule les changements non commit
- `/deploy [message]` : commit & push

## Sécurité (user_id + PIN)
- **Verrouillage user_id** : seules les commandes provenant de `ALLOWED_USER_ID` sont acceptées.
- **PIN optionnel** : si `ACCESS_PIN` est défini, le bot exige `/pin <code>` avant les actions sensibles.
- **Zero data leak** : aucune clé/token/chemin personnel n’est hardcodé dans le code ; tout passe par `.env`.

## Lier le bot à ton GitHub
1) Ajoute un remote :
```bash
git remote add origin https://github.com/<user>/<repo>.git
```
2) Assure-toi que l’auth est OK (SSH ou HTTPS token) puis utilise `/deploy`.

## Landing page (optionnel)

Ce repo contient également une landing page React dans le dossier `landing/`, utilisée pour présenter le projet. Elle n'est **pas nécessaire** pour utiliser le bot.

> **Note** : Le dossier `landing/` est exclu des archives ZIP GitHub (via `.gitattributes`) pour garder le téléchargement focalisé sur le bot. Il reste disponible dans le repo pour un éventuel déploiement web.

## Open Source checklist
- `.env` ignoré (`.gitignore`)
- `venv/`, `__pycache__/`, `dist/`, `build/`, `.DS_Store` ignorés
- template public : `dot-env.example`

## Licence
MIT (à ajuster si besoin)
