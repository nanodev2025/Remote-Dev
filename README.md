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
├── main.py
├── requirements.txt
├── src/
│   ├── bot.py
│   ├── ai_handler.py
│   └── git_manager.py
├── landing/                 # landing page React (Vite + Tailwind)
└── dot-env.example          # template à copier en `.env` (voir section Configuration)
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

## Configuration (Zero Data Leak)
1) Copie le template :
```bash
cp dot-env.example .env
```

2) Édite `.env` et remplis :
- `TELEGRAM_TOKEN`
- `ALLOWED_USER_ID`
- (recommandé) `ACCESS_PIN`
- ton provider IA (`AI_PROVIDER`) + la clé associée
- `GITHUB_REPO_URL` (optionnel mais utile)
- `WORKSPACE_PATH` (par défaut `.`)

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

## Landing page (React)
```bash
cd landing
npm install
npm run dev
```

## Open Source checklist
- `.env` ignoré (`.gitignore`)
- `venv/`, `__pycache__/`, `dist/`, `build/`, `.DS_Store` ignorés
- template public : `dot-env.example`

## Licence
MIT (à ajuster si besoin)
