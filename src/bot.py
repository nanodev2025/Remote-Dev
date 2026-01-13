"""
Bot Telegram - Serveur qui écoute les messages et orchestre les modifications
"""

import os
import logging
import time
from typing import Optional
from functools import wraps

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
from telegram.constants import ParseMode

from .ai_handler import AIHandler
from .git_manager import GitManager

logger = logging.getLogger(__name__)


def authorized_only(func):
    """Décorateur pour restreindre l'accès aux utilisateurs autorisés."""
    @wraps(func)
    async def wrapper(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        if user_id != self.allowed_user_id:
            logger.warning(f"⚠️ Accès non autorisé: {user_id}")
            await update.message.reply_text(
                "🚫 Accès refusé. Tu n'es pas autorisé à utiliser ce bot."
            )
            return

        # Deuxième facteur optionnel: PIN (si ACCESS_PIN est défini)
        if self.access_pin and not self._is_pin_verified():
            # Autoriser /start, /help et /id même sans PIN
            cmd = (update.message.text or "").split()[0].lower() if update.message else ""
            if cmd not in ("/start", "/help", "/id", "/pin"):
                await update.message.reply_text(
                    "🔐 **PIN requis**\n\n"
                    "Envoie `/pin <ton_code>` pour déverrouiller l'accès.",
                    parse_mode=ParseMode.MARKDOWN
                )
                return

        return await func(self, update, context)
    return wrapper


class TelegramBot:
    """Bot Telegram pour le déploiement piloté par mobile."""

    def __init__(
        self,
        token: str,
        allowed_user_id: int,
        ai_handler: AIHandler,
        git_manager: GitManager,
        github_url: str = "",
        access_pin: Optional[str] = None,
        pin_ttl_seconds: int = 12 * 60 * 60,  # 12h
    ):
        """
        Initialise le bot Telegram.
        
        Args:
            token: Token du bot Telegram
            allowed_user_id: ID de l'utilisateur autorisé
            ai_handler: Handler pour l'IA
            git_manager: Manager pour les opérations Git
            github_url: URL du repo GitHub pour les liens
        """
        self.token = token
        self.allowed_user_id = allowed_user_id
        self.ai_handler = ai_handler
        self.git_manager = git_manager
        self.github_url = github_url
        self.app: Optional[Application] = None

        # PIN optionnel
        self.access_pin = (access_pin or os.getenv("ACCESS_PIN") or "").strip() or None
        self.pin_ttl_seconds = pin_ttl_seconds
        self._pin_verified_until: Optional[float] = None
        
        logger.info(f"🤖 Bot initialisé pour l'utilisateur: {allowed_user_id}")

    def _is_pin_verified(self) -> bool:
        """Retourne True si le PIN est vérifié et encore valide."""
        if not self.access_pin:
            return True
        if not self._pin_verified_until:
            return False
        return time.time() < self._pin_verified_until

    def _mark_pin_verified(self) -> None:
        if not self.access_pin:
            return
        self._pin_verified_until = time.time() + self.pin_ttl_seconds

    def _setup_handlers(self) -> None:
        """Configure les handlers de commandes et messages."""
        # Commandes
        self.app.add_handler(CommandHandler("start", self._cmd_start))
        self.app.add_handler(CommandHandler("help", self._cmd_help))
        self.app.add_handler(CommandHandler("status", self._cmd_status))
        self.app.add_handler(CommandHandler("diff", self._cmd_diff))
        self.app.add_handler(CommandHandler("deploy", self._cmd_deploy))
        self.app.add_handler(CommandHandler("reset", self._cmd_reset))
        self.app.add_handler(CommandHandler("id", self._cmd_id))
        self.app.add_handler(CommandHandler("pin", self._cmd_pin))
        
        # Messages texte (instructions)
        self.app.add_handler(
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                self._handle_instruction
            )
        )
        
        logger.info("✅ Handlers configurés")

    async def _cmd_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Commande /start - Message de bienvenue."""
        user = update.effective_user
        is_authorized = user.id == self.allowed_user_id
        
        if is_authorized:
            pin_line = ""
            if self.access_pin:
                pin_line = (
                    "\n🔐 **PIN activé** : envoie `/pin <ton_code>` pour déverrouiller "
                    f"(valide {self.pin_ttl_seconds//3600}h).\n"
                )
            await update.message.reply_text(
                f"👋 Salut {user.first_name}!\n\n"
                "🚀 Je suis ton agent de déploiement. Envoie-moi des instructions "
                "en langage naturel et je modifierai ton code.\n\n"
                f"{pin_line}\n"
                "📝 Exemples:\n"
                "• \"Ajoute une fonction hello_world dans main.py\"\n"
                "• \"Crée un fichier utils/helpers.py avec des fonctions utilitaires\"\n"
                "• \"Corrige le bug dans la fonction calculate\"\n\n"
                "📚 Utilise /help pour voir toutes les commandes."
            )
        else:
            await update.message.reply_text(
                "🚫 Désolé, tu n'es pas autorisé à utiliser ce bot.\n"
                f"Ton ID: `{user.id}`",
                parse_mode=ParseMode.MARKDOWN
            )

    @authorized_only
    async def _cmd_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Commande /help - Liste des commandes."""
        pin_help = ""
        if self.access_pin:
            pin_help = "🔹 /pin <code> - Déverrouiller l'accès avec le PIN\n"
        await update.message.reply_text(
            "📚 **Commandes disponibles:**\n\n"
            "🔹 /start - Message de bienvenue\n"
            "🔹 /help - Cette aide\n"
            "🔹 /status - Statut Git du projet\n"
            "🔹 /diff - Voir les modifications en attente\n"
            "🔹 /deploy - Commit et push les modifications\n"
            "🔹 /reset - Annuler toutes les modifications\n"
            "🔹 /id - Afficher ton ID Telegram\n"
            f"{pin_help}\n"
            "💬 **Pour modifier le code:**\n"
            "Envoie simplement un message décrivant ce que tu veux faire!",
            parse_mode=ParseMode.MARKDOWN
        )

    @authorized_only
    async def _cmd_pin(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Commande /pin - Vérifie le PIN et déverrouille l'accès."""
        if not self.access_pin:
            await update.message.reply_text("ℹ️ Aucun PIN n'est configuré côté serveur.")
            return
        provided = " ".join(context.args).strip() if context.args else ""
        if not provided:
            await update.message.reply_text("🔐 Usage: `/pin <ton_code>`", parse_mode=ParseMode.MARKDOWN)
            return
        if provided != self.access_pin:
            await update.message.reply_text("❌ PIN incorrect.")
            return
        self._mark_pin_verified()
        await update.message.reply_text("✅ PIN validé. Accès déverrouillé.")

    @authorized_only
    async def _cmd_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Commande /status - Statut Git."""
        status = self.git_manager.get_status()
        await update.message.reply_text(f"📊 **Statut Git:**\n\n{status}", parse_mode=ParseMode.MARKDOWN)

    @authorized_only
    async def _cmd_diff(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Commande /diff - Affiche les différences."""
        diff = self.git_manager.get_detailed_diff(max_lines=40)
        
        # Telegram a une limite de 4096 caractères
        if len(diff) > 3900:
            diff = diff[:3900] + "\n\n... (tronqué)"
        
        await update.message.reply_text(
            f"📝 **Modifications:**\n\n```\n{diff}\n```",
            parse_mode=ParseMode.MARKDOWN
        )

    @authorized_only
    async def _cmd_deploy(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Commande /deploy - Commit et push."""
        await update.message.reply_text("🚀 Déploiement en cours...")
        
        # Récupérer le message de commit personnalisé si fourni
        commit_msg = " ".join(context.args) if context.args else "Update via Mobile Telegram"
        
        success, report = self.git_manager.deploy(commit_msg)
        
        if success and self.github_url:
            commit_url = self.git_manager.get_last_commit_url(self.github_url)
            if commit_url:
                report += f"\n\n🔗 [Voir le commit]({commit_url})"
        
        await update.message.reply_text(
            report,
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True
        )

    @authorized_only
    async def _cmd_reset(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Commande /reset - Annule les modifications."""
        success, msg = self.git_manager.reset_changes()
        await update.message.reply_text(msg)

    async def _cmd_id(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Commande /id - Affiche l'ID de l'utilisateur."""
        user = update.effective_user
        await update.message.reply_text(
            f"👤 **Ton profil:**\n\n"
            f"• ID: `{user.id}`\n"
            f"• Nom: {user.full_name}\n"
            f"• Username: @{user.username or 'N/A'}",
            parse_mode=ParseMode.MARKDOWN
        )

    @authorized_only
    async def _handle_instruction(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Traite une instruction en langage naturel."""
        instruction = update.message.text
        
        # Feedback immédiat
        processing_msg = await update.message.reply_text(
            "🤔 Analyse de l'instruction en cours..."
        )
        
        try:
            # Appeler l'IA pour interpréter l'instruction
            ai_response = await self.ai_handler.process_instruction(instruction)
            
            if not ai_response.success:
                await processing_msg.edit_text(
                    f"❌ **Erreur:**\n{ai_response.error or 'Impossible de traiter cette instruction'}"
                )
                return
            
            # Afficher les opérations prévues
            operations_text = "\n".join([
                f"• {op.action}: `{op.file_path}` - {op.description}"
                for op in ai_response.operations
            ])
            
            await processing_msg.edit_text(
                f"🔧 **Modifications prévues:**\n{operations_text}\n\n"
                f"📝 {ai_response.explanation}\n\n"
                "⏳ Application en cours...",
                parse_mode=ParseMode.MARKDOWN
            )
            
            # Appliquer les opérations
            results = self.ai_handler.apply_operations(ai_response.operations)
            
            # Vérifier si toutes les opérations ont réussi
            all_success = all(r["success"] for r in results)
            
            if all_success:
                # Construire le rapport de succès
                success_report = "\n".join([
                    f"✅ {r['action']}: `{r['file']}`"
                    for r in results
                ])
                
                # Récupérer le diff
                diff = self.git_manager.get_diff(staged=False)
                
                await processing_msg.edit_text(
                    f"✨ **Modifications appliquées!**\n\n"
                    f"{success_report}\n\n"
                    f"📊 **Diff:**\n```\n{diff[:1500]}\n```\n\n"
                    "💡 Utilise /deploy pour pusher ou /reset pour annuler.",
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                # Rollback en cas d'erreur
                self.ai_handler.rollback_operations(ai_response.operations)
                self.git_manager.reset_changes()
                
                error_report = "\n".join([
                    f"{'✅' if r['success'] else '❌'} {r['action']}: {r['file']}"
                    + (f" - {r['error']}" if r.get('error') else "")
                    for r in results
                ])
                
                await processing_msg.edit_text(
                    f"❌ **Erreur lors de l'application:**\n\n{error_report}\n\n"
                    "↩️ Les modifications ont été annulées.",
                    parse_mode=ParseMode.MARKDOWN
                )
                
        except Exception as e:
            logger.error(f"Erreur traitement instruction: {e}")
            await processing_msg.edit_text(
                f"❌ **Erreur inattendue:**\n`{str(e)}`",
                parse_mode=ParseMode.MARKDOWN
            )

    def run(self) -> None:
        """Démarre le bot (bloquant)."""
        import asyncio
        
        self.app = Application.builder().token(self.token).build()
        self._setup_handlers()
        
        logger.info("🚀 Démarrage du bot...")
        
        # Supprimer le webhook s'il existe pour éviter les conflits
        async def delete_webhook():
            try:
                await self.app.bot.delete_webhook(drop_pending_updates=True)
                logger.info("✅ Webhook supprimé (si présent)")
            except Exception as e:
                logger.warning(f"⚠️ Impossible de supprimer le webhook: {e}")
        
        # Créer un event loop pour Python 3.10+
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        # Supprimer le webhook avant de démarrer le polling
        try:
            loop.run_until_complete(delete_webhook())
            # Attendre un peu pour que Telegram synchronise
            import time
            time.sleep(2)
        except Exception as e:
            logger.warning(f"⚠️ Erreur lors de la suppression du webhook: {e}")
        
        # Démarrer le polling avec gestion d'erreur pour les conflits
        try:
            self.app.run_polling(
                allowed_updates=Update.ALL_TYPES, 
                drop_pending_updates=True,
                close_loop=False
            )
        except Exception as e:
            if "Conflict" in str(e):
                logger.error("❌ Conflit détecté. Attente de 5 secondes puis nouvelle tentative...")
                import time
                time.sleep(5)
                # Nouvelle tentative
                loop.run_until_complete(delete_webhook())
                time.sleep(2)
                self.app.run_polling(
                    allowed_updates=Update.ALL_TYPES, 
                    drop_pending_updates=True
                )
            else:
                raise

    async def start_async(self) -> None:
        """Démarre le bot de manière asynchrone."""
        self.app = Application.builder().token(self.token).build()
        self._setup_handlers()
        
        await self.app.initialize()
        await self.app.start()
        await self.app.updater.start_polling(allowed_updates=Update.ALL_TYPES)
        
        logger.info("🚀 Bot démarré en mode asynchrone")

    async def stop_async(self) -> None:
        """Arrête le bot de manière asynchrone."""
        if self.app:
            await self.app.updater.stop()
            await self.app.stop()
            await self.app.shutdown()
            logger.info("🛑 Bot arrêté")
