#!/usr/bin/env python3
"""
MyBotCursor - Agent de déploiement piloté par Telegram
Point d'entrée principal
"""

import os
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('bot.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)


def validate_env() -> dict:
    """
    Valide et retourne les variables d'environnement requises.
    
    Returns:
        dict avec les configurations
        
    Raises:
        ValueError si des variables sont manquantes
    """
    required_vars = {
        "TELEGRAM_TOKEN": os.getenv("TELEGRAM_TOKEN"),
        "ALLOWED_USER_ID": os.getenv("ALLOWED_USER_ID"),
    }
    
    # Vérifier les variables obligatoires
    missing = [k for k, v in required_vars.items() if not v]
    if missing:
        raise ValueError(f"Variables d'environnement manquantes: {', '.join(missing)}")
    
    # Configuration IA
    ai_provider = os.getenv("AI_PROVIDER", "gemini").lower()
    if ai_provider == "anthropic":
        if not os.getenv("ANTHROPIC_API_KEY"):
            raise ValueError("ANTHROPIC_API_KEY requise quand AI_PROVIDER=anthropic")
    elif ai_provider == "openai":
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY requise quand AI_PROVIDER=openai")
    elif ai_provider == "groq":
        if not os.getenv("GROQ_API_KEY"):
            raise ValueError("GROQ_API_KEY requise quand AI_PROVIDER=groq\n"
                           "👉 Obtiens ta clé gratuite sur: https://console.groq.com/keys")
    elif ai_provider == "gemini":
        if not os.getenv("GEMINI_API_KEY"):
            raise ValueError("GEMINI_API_KEY requise quand AI_PROVIDER=gemini\n"
                           "👉 Obtiens ta clé gratuite sur: https://aistudio.google.com/apikey")
    elif ai_provider == "ollama":
        pass  # Ollama n'a pas besoin de clé API
    else:
        raise ValueError(f"AI_PROVIDER invalide: {ai_provider}. Utilise 'gemini', 'groq', 'ollama', 'anthropic' ou 'openai'")
    
    return {
        "telegram_token": required_vars["TELEGRAM_TOKEN"],
        "allowed_user_id": int(required_vars["ALLOWED_USER_ID"]),
        "access_pin": (os.getenv("ACCESS_PIN") or "").strip() or None,
        "ai_provider": ai_provider,
        "git_branch": os.getenv("GIT_BRANCH", "main"),
        "github_url": os.getenv("GITHUB_REPO_URL", ""),
        "workspace_path": os.getenv("WORKSPACE_PATH", os.getcwd()),
    }


def main():
    """Point d'entrée principal."""
    # Charger les variables d'environnement
    # Évite `find_dotenv()` (instable selon les versions de Python) en pointant explicitement vers `.env`
    load_dotenv(dotenv_path=Path(__file__).with_name(".env"))
    
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║   🤖 MyBotCursor - Agent de Déploiement Telegram             ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    try:
        # Valider la configuration
        config = validate_env()
        logger.info("✅ Configuration validée")
        logger.info(f"   • Provider IA: {config['ai_provider']}")
        logger.info(f"   • Branche Git: {config['git_branch']}")
        logger.info(f"   • Workspace: {config['workspace_path']}")
        
        # Importer les modules
        from src.ai_handler import AIHandler
        from src.git_manager import GitManager
        from src.bot import TelegramBot
        
        # Initialiser les composants
        ai_handler = AIHandler(
            provider=config["ai_provider"],
            workspace_path=config["workspace_path"]
        )
        logger.info("✅ AI Handler initialisé")
        
        git_manager = GitManager(
            workspace_path=config["workspace_path"],
            branch=config["git_branch"]
        )
        logger.info("✅ Git Manager initialisé")
        
        # Créer et démarrer le bot
        bot = TelegramBot(
            token=config["telegram_token"],
            allowed_user_id=config["allowed_user_id"],
            ai_handler=ai_handler,
            git_manager=git_manager,
            github_url=config["github_url"],
            access_pin=config["access_pin"],
        )
        
        logger.info("🚀 Démarrage du bot Telegram...")
        logger.info("   Appuie sur Ctrl+C pour arrêter")
        
        bot.run()
        
    except ValueError as e:
        logger.error(f"❌ Erreur de configuration: {e}")
        print(f"\n⚠️  Erreur: {e}")
        print("\n📋 Vérifie ton fichier .env avec les variables suivantes:")
        print("   - TELEGRAM_TOKEN")
        print("   - ALLOWED_USER_ID")
        print("   - AI_PROVIDER (gemini | groq | openai | anthropic | ollama)")
        print("   - Clé API selon le provider choisi:")
        print("     • GEMINI_API_KEY (gemini - gratuit)")
        print("     • GROQ_API_KEY (groq - gratuit)")
        print("     • OPENAI_API_KEY (openai)")
        print("     • ANTHROPIC_API_KEY (anthropic)")
        print("     • (aucune pour ollama)")
        print("   - WORKSPACE_PATH (optionnel)")
        print("   - GIT_BRANCH (optionnel, défaut: main)")
        print("   - GITHUB_REPO_URL (optionnel)")
        sys.exit(1)
        
    except KeyboardInterrupt:
        logger.info("\n👋 Arrêt du bot...")
        sys.exit(0)
        
    except Exception as e:
        logger.exception(f"❌ Erreur inattendue: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
