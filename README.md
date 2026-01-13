# Remote Dev — Telegram‑driven code & deploy agent

Bot Telegram qui te permet de piloter des modifications de code depuis ton mobile, puis de versionner (commit) et publier (push) automatiquement.

## ✅ Compatibilité

**Multi-plateforme** : Fonctionne sur **tous les systèmes** avec Python 3.9+ :
- ✅ **Windows** (10/11)
- ✅ **macOS** (10.15+)
- ✅ **Linux** (toutes distributions)
- ✅ **Raspberry Pi** (Zero, 3, 4, 5)
- ✅ **VPS** (DigitalOcean, AWS, Hetzner, etc.)
- ✅ **Serveurs cloud** (Docker, WSL2)

**Prérequis minimaux** :
- Python **3.9+** (3.11+ recommandé)
- **512 MB RAM** minimum
- **100 MB** d'espace disque
- Connexion internet stable
- Git installé (pour les opérations Git)

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

## 🚀 Installation rapide

### Option 1 : Script automatique (recommandé)

**Linux / macOS :**
```bash
git clone https://github.com/nanodev2025/Remote-Dev.git
cd Remote-Dev
./install.sh
```

**Windows :**
```cmd
git clone https://github.com/nanodev2025/Remote-Dev.git
cd Remote-Dev
install.bat
```

Le script installe automatiquement les dépendances et crée le fichier `.env` (vide) à partir du template. Tu devras ensuite éditer `.env` pour y ajouter tes clés API.

### Option 2 : Installation manuelle

```bash
git clone https://github.com/nanodev2025/Remote-Dev.git
cd Remote-Dev

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp dot-env.example .env
```

## ⚙️ Configuration minimale

### 1. Créer ton bot Telegram

1. **Ouvre Telegram** et cherche `@BotFather`
2. **Envoie** `/newbot` et suis les instructions
3. **Choisis un nom** pour ton bot (ex: "Mon Dev Bot")
4. **Choisis un username** (doit finir par `bot`, ex: `mon_dev_bot`)
5. **Copie le token** que BotFather te donne (format: `123456789:ABCdef...`)

### 2. Obtenir ton user_id Telegram

1. **Ouvre Telegram** et cherche `@userinfobot`
2. **Envoie** `/start`
3. **Copie ton ID** (un nombre, ex: `123456789`)

### 3. Configurer le fichier `.env`

Édite `.env` et remplis **uniquement** ces 4 valeurs essentielles :

```bash
# 1. Telegram (obligatoire)
TELEGRAM_TOKEN=123456789:ABCdef...     # Token copié depuis @BotFather
ALLOWED_USER_ID=123456789              # Ton ID copié depuis @userinfobot

# 2. IA (obligatoire - choisis UN provider gratuit)
AI_PROVIDER=gemini                      # ou groq, ollama
GEMINI_API_KEY=ta_cle_ici               # Gratuit : https://aistudio.google.com/apikey
```

**C'est tout !** Les autres variables sont optionnelles et ont des valeurs par défaut.

> 💡 **Optionnel** : `ACCESS_PIN` pour sécurité renforcée, `GITHUB_REPO_URL` pour les liens de commit, `WORKSPACE_PATH` si tu veux modifier un autre projet.

## ▶️ Démarrage

Une fois le `.env` configuré avec tes clés API :

**Linux / macOS :**
```bash
source venv/bin/activate  # Si pas déjà activé
python main.py
```

**Windows :**
```cmd
venv\Scripts\activate
python main.py
```

Tu devrais voir :
```
🚀 Démarrage du bot...
✅ Configuration validée
🤖 Bot initialisé pour l'utilisateur: 123456789
```

**Teste le bot** : Ouvre Telegram, cherche ton bot par son username, et envoie `/start`. Le bot devrait répondre !

> ⚠️ **Important** : Le bot doit rester en cours d'exécution pour fonctionner. Si tu fermes le terminal, le bot s'arrête. Pour le faire tourner en arrière-plan, utilise `systemd` (voir section "Déploiement sur serveur").

## 📋 Configuration avancée

<details>
<summary>Voir toutes les options de configuration</summary>

### Variables optionnelles

- `ACCESS_PIN` : Code PIN optionnel pour sécurité renforcée
- `GITHUB_REPO_URL` : URL de ton repo GitHub (pour liens de commit dans Telegram)
- `WORKSPACE_PATH` : Chemin vers le projet à modifier (par défaut `.`)
- `GIT_BRANCH` : Branche Git (par défaut `main`)

### Providers IA disponibles

- **Gemini** (gratuit) : `AI_PROVIDER=gemini` + `GEMINI_API_KEY`
- **Groq** (gratuit) : `AI_PROVIDER=groq` + `GROQ_API_KEY`
- **Ollama** (local, gratuit) : `AI_PROVIDER=ollama` (pas de clé nécessaire)
- **OpenAI** (payant) : `AI_PROVIDER=openai` + `OPENAI_API_KEY`
- **Anthropic** (payant) : `AI_PROVIDER=anthropic` + `ANTHROPIC_API_KEY`

</details>

## Déploiement sur serveur (Raspberry Pi / VPS)

### Installation sur Linux (Raspberry Pi, VPS, etc.)

Le bot fonctionne sur n'importe quel serveur Linux avec Python 3.9+ (3.11+ recommandé) :

```bash
# 1. Cloner le repository
git clone https://github.com/nanodev2025/Remote-Dev.git
cd Remote-Dev

# 2. Vérifier Python (3.9+ requis, 3.11+ recommandé)
python3 --version

# Si Python < 3.9, installer Python 3.9+ :
# Ubuntu/Debian :
sudo apt update
sudo apt install python3.9 python3.9-venv python3-pip
# Ou Python 3.11+ (recommandé) :
sudo apt install python3.11 python3.11-venv python3-pip

# 3. Créer l'environnement virtuel et installer les dépendances
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 4. Configurer le .env
cp dot-env.example .env
nano .env  # Remplir avec tes clés API
```

### Configuration du WORKSPACE_PATH

Par défaut, le bot modifie les fichiers dans son propre répertoire. Si tu veux qu'il modifie un autre projet :

1. **Option 1 : Répertoire courant**
   ```bash
   # Dans .env, laisse vide ou utilise :
   WORKSPACE_PATH=.
   ```

2. **Option 2 : Autre projet Git**
   ```bash
   # Dans .env, configure le chemin vers TON propre projet :
   WORKSPACE_PATH=/chemin/vers/ton/projet
   
   # Le projet cible doit être un dépôt Git initialisé :
   cd /chemin/vers/ton/projet
   git init
   
   # ⚠️ IMPORTANT : Ajoute TON propre repository GitHub (pas Remote-Dev !)
   git remote add origin https://github.com/TON-USERNAME/TON-REPO.git
   
   # Le bot modifiera les fichiers de ce projet et poussera vers TON repo
   ```

### Lancer le bot au démarrage (systemd)

Pour que le bot démarre automatiquement au boot du serveur :

1. **Créer le service systemd** :
   ```bash
   sudo nano /etc/systemd/system/remote-dev-bot.service
   ```

2. **Ajouter cette configuration** (remplace `/home/pi/Remote-Dev` par ton chemin) :
   ```ini
   [Unit]
   Description=Remote Dev Telegram Bot
   After=network.target

   [Service]
   Type=simple
   User=pi
   WorkingDirectory=/home/pi/Remote-Dev
   Environment="PATH=/home/pi/Remote-Dev/venv/bin"
   ExecStart=/home/pi/Remote-Dev/venv/bin/python3 main.py
   Restart=always
   RestartSec=10

   [Install]
   WantedBy=multi-user.target
   ```

3. **Activer et démarrer le service** :
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable remote-dev-bot
   sudo systemctl start remote-dev-bot
   
   # Vérifier le statut
   sudo systemctl status remote-dev-bot
   
   # Voir les logs
   journalctl -u remote-dev-bot -f
   ```

### Notes pour serveurs payants (VPS)

- **Firewall** : Aucune ouverture de port nécessaire (le bot utilise l'API Telegram)
- **RAM** : 512 MB minimum (256 MB possible sur Raspberry Pi Zero)
- **Stockage** : ~100 MB pour le bot + espace pour tes projets
- **CPU** : Très léger, fonctionne même sur Raspberry Pi Zero (ARM)
- **Réseau** : Connexion internet stable requise pour l'API Telegram et les APIs IA
- **OS** : Compatible avec toutes les distributions Linux récentes (Ubuntu, Debian, Fedora, Arch, etc.)

### Logs

Les logs sont écrits dans `bot.log` dans le répertoire du bot, et également dans les logs systemd :

```bash
# Logs du fichier
tail -f bot.log

# Logs systemd (si configuré comme service)
journalctl -u remote-dev-bot -f
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

### Si WORKSPACE_PATH=. (bot modifie Remote-Dev lui-même)

1) Ajoute un remote au projet Remote-Dev :
```bash
cd Remote-Dev
git remote add origin https://github.com/TON-USERNAME/TON-FORK-REPO.git
```

### Si WORKSPACE_PATH pointe vers un autre projet

Le projet cible doit avoir son propre `remote origin` pointant vers **TON** repository GitHub (pas Remote-Dev !). Voir la section "Configuration du WORKSPACE_PATH" ci-dessus.

### Authentication

Assure-toi que l'auth Git est OK (SSH ou HTTPS token) puis utilise `/deploy` dans Telegram.
## Licence
MIT
