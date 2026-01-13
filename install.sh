#!/bin/bash
# Script d'installation automatique pour Remote Dev Bot

set -e

echo "🚀 Installation de Remote Dev Bot..."
echo ""

# Vérifier Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé. Installe Python 3.9+ puis relance ce script."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
PYTHON_MAJOR=$(python3 -c 'import sys; print(sys.version_info[0])')
PYTHON_MINOR=$(python3 -c 'import sys; print(sys.version_info[1])')

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 9 ]); then
    echo "❌ Python 3.9+ requis. Version détectée: $PYTHON_VERSION"
    echo "   Installe Python 3.9+ puis relance ce script."
    exit 1
fi

echo "✅ Python $PYTHON_VERSION détecté (3.9+ requis, 3.11+ recommandé)"

# Créer venv
if [ ! -d "venv" ]; then
    echo "📦 Création de l'environnement virtuel..."
    python3 -m venv venv
fi

# Activer venv
echo "🔧 Activation de l'environnement virtuel..."
source venv/bin/activate

# Installer les dépendances
echo "📥 Installation des dépendances..."
pip install --upgrade pip
pip install -r requirements.txt

# Créer .env si n'existe pas
if [ ! -f ".env" ]; then
    echo "📝 Création du fichier .env..."
    cp dot-env.example .env
    echo "✅ Fichier .env créé depuis dot-env.example"
    echo ""
    echo "⚠️  IMPORTANT : Édite le fichier .env et remplis :"
    echo "   - TELEGRAM_TOKEN (obtenu via @BotFather)"
    echo "   - ALLOWED_USER_ID (obtenu via @userinfobot)"
    echo "   - AI_PROVIDER (gemini, groq, ollama, openai, ou anthropic)"
    echo "   - La clé API correspondante (GEMINI_API_KEY, GROQ_API_KEY, etc.)"
    echo ""
    echo "💡 Pour démarrer le bot :"
    echo "   source venv/bin/activate"
    echo "   python main.py"
else
    echo "✅ Fichier .env existe déjà"
fi

echo ""
echo "✨ Installation terminée !"
echo ""
echo "📋 Prochaines étapes :"
echo "   1. Édite .env avec tes clés API"
echo "   2. Lance le bot : source venv/bin/activate && python main.py"
