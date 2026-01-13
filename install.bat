@echo off
REM Script d'installation automatique pour Remote Dev Bot (Windows)

echo 🚀 Installation de Remote Dev Bot...
echo.

REM Vérifier Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python n'est pas installé. Installe Python 3.9+ puis relance ce script.
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ Python %PYTHON_VERSION% détecté (3.9+ requis, 3.11+ recommandé)

REM Créer venv
if not exist "venv" (
    echo 📦 Création de l'environnement virtuel...
    python -m venv venv
)

REM Activer venv
echo 🔧 Activation de l'environnement virtuel...
call venv\Scripts\activate.bat

REM Installer les dépendances
echo 📥 Installation des dépendances...
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Créer .env si n'existe pas
if not exist ".env" (
    echo 📝 Création du fichier .env...
    copy dot-env.example .env
    echo ✅ Fichier .env créé depuis dot-env.example
    echo.
    echo ⚠️  IMPORTANT : Édite le fichier .env et remplis :
    echo    - TELEGRAM_TOKEN (obtenu via @BotFather)
    echo    - ALLOWED_USER_ID (obtenu via @userinfobot)
    echo    - AI_PROVIDER (gemini, groq, ollama, openai, ou anthropic)
    echo    - La clé API correspondante (GEMINI_API_KEY, GROQ_API_KEY, etc.)
    echo.
    echo 💡 Pour démarrer le bot :
    echo    venv\Scripts\activate
    echo    python main.py
) else (
    echo ✅ Fichier .env existe déjà
)

echo.
echo ✨ Installation terminée !
echo.
echo 📋 Prochaines étapes :
echo    1. Édite .env avec tes clés API
echo    2. Lance le bot : venv\Scripts\activate && python main.py
pause
