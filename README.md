# 🤖 MyBotCursor - Agent de Déploiement Telegram

Un bot Telegram intelligent qui te permet de modifier ton code depuis ton mobile en utilisant des instructions en langage naturel, puis de déployer automatiquement les changements via Git.

## ✨ Fonctionnalités

- 📱 **Contrôle depuis Telegram** - Envoie des instructions depuis ton mobile
- 🧠 **IA intégrée** - Utilise Claude (Anthropic) ou GPT-4 (OpenAI) pour interpréter tes instructions
- 🔐 **Sécurisé** - Accès restreint par ID utilisateur Telegram
- 🔄 **Git automatisé** - Add, commit et push automatiques
- 📊 **Feedback en temps réel** - Diff du code et liens vers les commits
- ↩️ **Rollback sécurisé** - Annulation automatique en cas d'erreur

## 📁 Structure du Projet

```
MyBotCursor/
├── main.py              # Point d'entrée
├── requirements.txt     # Dépendances Python
├── env.example          # Template de configuration
├── README.md            # Documentation
└── src/
    ├── __init__.py
    ├── bot.py           # Serveur Bot Telegram
    ├── ai_handler.py    # Logique IA (OpenAI/Claude)
    └── git_manager.py   # Gestionnaire Git
```

## 🚀 Installation

### 1. Cloner et configurer l'environnement

```bash
cd /Users/EvilCorp/Documents/Dev/MyBotCursor

# Créer un environnement virtuel
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou: venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt
```

### 2. Configurer les variables d'environnement

```bash
# Copier le template
cp env.example .env

# Éditer le fichier .env avec tes valeurs
nano .env
```

### 3. Obtenir les tokens nécessaires

#### Token Telegram
1. Ouvre [@BotFather](https://t.me/BotFather) sur Telegram
2. Envoie `/newbot` et suis les instructions
3. Copie le token fourni

#### Ton ID Telegram
1. Ouvre [@userinfobot](https://t.me/userinfobot) sur Telegram
2. Envoie `/start`
3. Note ton ID utilisateur

#### Clé API IA
- **Anthropic (Claude)**: [console.anthropic.com](https://console.anthropic.com/)
- **OpenAI (GPT-4)**: [platform.openai.com](https://platform.openai.com/)

### 4. Configurer Git

Assure-toi que ton repo est configuré avec un remote `origin`:

```bash
git remote -v
# Si pas de remote:
git remote add origin https://github.com/ton-username/ton-repo.git
```

### 5. Lancer le bot

```bash
python main.py
```

## 📱 Utilisation

### Commandes Telegram

| Commande | Description |
|----------|-------------|
| `/start` | Message de bienvenue |
| `/help` | Liste des commandes |
| `/status` | Statut Git du projet |
| `/diff` | Voir les modifications en attente |
| `/deploy [message]` | Commit et push (message optionnel) |
| `/reset` | Annuler toutes les modifications |
| `/id` | Afficher ton ID Telegram |

### Exemples d'instructions

```
Crée un fichier hello.py avec une fonction qui dit bonjour

Ajoute une méthode calculate_total dans la classe Order

Modifie le fichier config.py pour ajouter une variable DEBUG=True

Corrige le bug dans la fonction parse_date qui ne gère pas les fuseaux horaires
```

## ⚙️ Configuration (.env)

```env
# Telegram
TELEGRAM_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
ALLOWED_USER_ID=123456789

# IA (choisir un)
AI_PROVIDER=anthropic  # ou "openai"
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...

# Git
GIT_BRANCH=main
GITHUB_REPO_URL=https://github.com/username/repo

# Workspace
WORKSPACE_PATH=/chemin/vers/ton/projet
```

## 🔒 Sécurité

- **Authentification**: Seul l'utilisateur avec l'ID spécifié peut utiliser le bot
- **Pas de push si erreur**: Les modifications ne sont poussées que si tout a réussi
- **Rollback automatique**: En cas d'erreur, les changements sont annulés
- **Logs**: Toutes les actions sont enregistrées dans `bot.log`

## 🐛 Dépannage

### Le bot ne répond pas
- Vérifie que le token Telegram est correct
- Vérifie que le bot est démarré (`python main.py`)

### "Accès refusé"
- Vérifie que ton `ALLOWED_USER_ID` correspond à ton ID Telegram
- Utilise `/id` pour voir ton ID

### Erreur de push Git
- Vérifie que tu as les droits de push sur le repo
- Vérifie que le remote `origin` est configuré
- Assure-toi d'avoir configuré l'authentification Git (SSH ou HTTPS)

### Erreur API IA
- Vérifie que ta clé API est valide
- Vérifie que tu as du crédit sur ton compte

## 📝 Logs

Les logs sont écrits dans:
- Console (stdout)
- Fichier `bot.log`

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésite pas à ouvrir une issue ou une PR.

## 📄 Licence

MIT License - Utilise ce code comme tu veux !
