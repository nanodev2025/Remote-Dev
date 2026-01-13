"""
Gestionnaire Git - Gère les opérations git (add, commit, push)
"""

import os
import logging
from typing import Optional, Tuple
from git import Repo, InvalidGitRepositoryError, GitCommandError, BadName

logger = logging.getLogger(__name__)


class GitManager:
    """Gère les opérations Git pour le déploiement automatique."""

    def __init__(self, workspace_path: str, branch: str = "main"):
        """
        Initialise le gestionnaire Git.
        
        Args:
            workspace_path: Chemin vers le répertoire de travail Git
            branch: Branche sur laquelle pousser les modifications
        """
        self.workspace_path = workspace_path
        self.branch = branch
        self.repo: Optional[Repo] = None
        self._init_repo()

    def _init_repo(self) -> None:
        """Initialise la connexion au dépôt Git."""
        try:
            self.repo = Repo(self.workspace_path)
            logger.info(f"✅ Dépôt Git initialisé: {self.workspace_path}")
        except InvalidGitRepositoryError:
            logger.error(f"❌ Pas de dépôt Git trouvé dans: {self.workspace_path}")
            raise ValueError(f"Le chemin {self.workspace_path} n'est pas un dépôt Git valide")

    def get_status(self) -> str:
        """Retourne le statut actuel du dépôt."""
        if not self.repo:
            return "❌ Dépôt non initialisé"
        
        status_lines = []
        
        # Fichiers modifiés
        changed = [item.a_path for item in self.repo.index.diff(None)]
        if changed:
            status_lines.append(f"📝 Modifiés: {', '.join(changed)}")
        
        # Fichiers non suivis
        untracked = self.repo.untracked_files
        if untracked:
            status_lines.append(f"🆕 Non suivis: {', '.join(untracked)}")
        
        # Fichiers stagés
        staged = [item.a_path for item in self.repo.index.diff("HEAD")]
        if staged:
            status_lines.append(f"✅ Stagés: {', '.join(staged)}")
        
        if not status_lines:
            return "✨ Répertoire de travail propre"
        
        return "\n".join(status_lines)

    def get_diff(self, staged: bool = True) -> str:
        """
        Retourne le diff des modifications.
        
        Args:
            staged: Si True, montre le diff des fichiers stagés
        """
        if not self.repo:
            return ""
        
        try:
            if staged:
                diff = self.repo.git.diff("--cached", "--stat")
            else:
                diff = self.repo.git.diff("--stat")
            
            if not diff:
                return "Aucune modification"
            
            return diff
        except GitCommandError as e:
            logger.error(f"Erreur lors de la récupération du diff: {e}")
            return f"Erreur: {str(e)}"

    def get_detailed_diff(self, max_lines: int = 50) -> str:
        """Retourne un diff détaillé (limité en taille pour Telegram)."""
        if not self.repo:
            return ""
        
        try:
            diff = self.repo.git.diff("--cached")
            lines = diff.split("\n")
            
            if len(lines) > max_lines:
                return "\n".join(lines[:max_lines]) + f"\n\n... (+{len(lines) - max_lines} lignes)"
            
            return diff if diff else "Aucune modification"
        except GitCommandError as e:
            return f"Erreur: {str(e)}"

    def stage_all(self) -> Tuple[bool, str]:
        """
        Stage tous les fichiers modifiés (git add .).
        
        Returns:
            Tuple (succès, message)
        """
        if not self.repo:
            return False, "❌ Dépôt non initialisé"
        
        try:
            self.repo.git.add(".")
            logger.info("✅ Tous les fichiers ont été stagés")
            return True, "✅ Fichiers stagés avec succès"
        except GitCommandError as e:
            logger.error(f"❌ Erreur lors du staging: {e}")
            return False, f"❌ Erreur: {str(e)}"

    def commit(self, message: str = "Update via Mobile Telegram") -> Tuple[bool, str]:
        """
        Crée un commit avec le message spécifié.
        
        Args:
            message: Message du commit
            
        Returns:
            Tuple (succès, message/hash du commit)
        """
        if not self.repo:
            return False, "❌ Dépôt non initialisé"
        
        try:
            # Vérifier s'il y a des changements stagés
            # Pour le premier commit, HEAD n'existe pas, donc on vérifie différemment
            has_staged_changes = False
            try:
                # Essayer de vérifier avec HEAD si des commits existent
                staged_changes = list(self.repo.index.diff("HEAD"))
                has_staged_changes = len(staged_changes) > 0
            except (ValueError, BadName):
                # Si HEAD n'existe pas (premier commit), vérifier directement les entrées de l'index
                has_staged_changes = len(self.repo.index.entries) > 0
            
            if not has_staged_changes:
                return False, "⚠️ Aucun changement à commiter"
            
            commit = self.repo.index.commit(message)
            commit_hash = commit.hexsha[:8]
            logger.info(f"✅ Commit créé: {commit_hash}")
            return True, f"✅ Commit: {commit_hash}"
        except GitCommandError as e:
            logger.error(f"❌ Erreur lors du commit: {e}")
            return False, f"❌ Erreur: {str(e)}"
        except Exception as e:
            logger.error(f"❌ Erreur inattendue lors du commit: {e}")
            return False, f"❌ Erreur: {str(e)}"

    def push(self) -> Tuple[bool, str]:
        """
        Pousse les modifications vers le dépôt distant.
        
        Returns:
            Tuple (succès, message)
        """
        if not self.repo:
            return False, "❌ Dépôt non initialisé"
        
        try:
            # Vérifier que la branche locale existe
            try:
                branch_ref = self.repo.heads[self.branch]
            except (IndexError, AttributeError):
                # Si la branche n'existe pas localement, utiliser la branche actuelle
                current_branch = self.repo.active_branch.name
                logger.warning(f"⚠️ Branche '{self.branch}' introuvable, utilisation de '{current_branch}'")
                branch_ref = self.repo.heads[current_branch]
                self.branch = current_branch
            
            origin = self.repo.remote("origin")
            
            # Vérifier si c'est le premier push (pas de branche distante)
            try:
                origin.fetch()
                remote_ref = f"origin/{self.branch}"
                # Si la branche distante n'existe pas, utiliser set_upstream
                if remote_ref not in [ref.name for ref in self.repo.refs]:
                    logger.info(f"🆕 Premier push vers {self.branch}, configuration upstream...")
                    push_info = origin.push(branch_ref, set_upstream=True)
                else:
                    push_info = origin.push(branch_ref)
            except Exception:
                # Si fetch échoue, essayer directement avec set_upstream
                logger.info(f"🆕 Premier push vers {self.branch}, configuration upstream...")
                push_info = origin.push(branch_ref, set_upstream=True)
            
            # Vérifier les résultats du push
            for info in push_info:
                if info.flags & info.ERROR:
                    error_msg = info.summary or str(info)
                    logger.error(f"❌ Erreur push: {error_msg}")
                    return False, f"❌ Erreur push: {error_msg}"
                elif info.flags & info.REJECTED:
                    logger.error(f"❌ Push rejeté: {info.summary}")
                    return False, f"❌ Push rejeté: {info.summary}"
            
            logger.info(f"✅ Push réussi vers {self.branch}")
            return True, f"✅ Push vers origin/{self.branch} réussi"
        except GitCommandError as e:
            error_msg = str(e)
            logger.error(f"❌ Erreur lors du push: {error_msg}")
            
            # Messages d'erreur plus explicites
            if "authentication" in error_msg.lower() or "permission" in error_msg.lower():
                return False, "❌ Erreur d'authentification. Vérifiez vos credentials Git."
            elif "not found" in error_msg.lower() or "does not exist" in error_msg.lower():
                return False, f"❌ Branche '{self.branch}' introuvable sur le remote."
            else:
                return False, f"❌ Erreur: {error_msg}"
        except Exception as e:
            logger.error(f"❌ Erreur inattendue lors du push: {e}")
            return False, f"❌ Erreur: {str(e)}"

    def deploy(self, commit_message: str = "Update via Mobile Telegram") -> Tuple[bool, str]:
        """
        Exécute le workflow complet: add -> commit -> push.
        
        Args:
            commit_message: Message du commit
            
        Returns:
            Tuple (succès, rapport détaillé)
        """
        report = []
        
        # Étape 1: Stage
        success, msg = self.stage_all()
        report.append(f"1️⃣ Stage: {msg}")
        if not success:
            return False, "\n".join(report)
        
        # Récupérer le diff avant commit
        diff = self.get_diff(staged=True)
        
        # Étape 2: Commit
        success, msg = self.commit(commit_message)
        report.append(f"2️⃣ Commit: {msg}")
        if not success:
            return False, "\n".join(report)
        
        # Étape 3: Push
        success, msg = self.push()
        report.append(f"3️⃣ Push: {msg}")
        
        if success:
            report.append(f"\n📊 Diff:\n```\n{diff}\n```")
            report.append(f"\n🔗 Branche: {self.branch}")
        
        return success, "\n".join(report)

    def get_last_commit_url(self, github_url: str) -> str:
        """
        Génère l'URL du dernier commit sur GitHub.
        
        Args:
            github_url: URL du dépôt GitHub
        """
        if not self.repo:
            return ""
        
        try:
            commit_hash_full = self.repo.head.commit.hexsha
            # Utiliser un hash court (7 caractères) pour l'URL GitHub
            commit_hash = commit_hash_full[:7]
            
            # Nettoyer l'URL GitHub
            # Supprimer .git à la fin si présent
            base_url = github_url.rstrip(".git")
            # Supprimer le slash final si présent
            base_url = base_url.rstrip("/")
            
            # S'assurer que l'URL est bien formatée
            # Si l'URL contient déjà /commit/, on la nettoie
            if "/commit/" in base_url:
                base_url = base_url.split("/commit/")[0]
            
            # Supprimer tout hash existant à la fin de l'URL
            # Au cas où l'URL contiendrait déjà un hash
            if len(base_url.split("/")[-1]) == 40 or len(base_url.split("/")[-1]) == 7:
                # Si le dernier segment ressemble à un hash, le supprimer
                parts = base_url.split("/")
                if parts[-1] and (len(parts[-1]) == 40 or (len(parts[-1]) == 7 and all(c in '0123456789abcdef' for c in parts[-1].lower()))):
                    base_url = "/".join(parts[:-1])
            
            # Construire l'URL du commit
            commit_url = f"{base_url}/commit/{commit_hash}"
            
            logger.info(f"🔗 URL générée: {commit_url}")
            return commit_url
        except Exception as e:
            logger.error(f"Erreur lors de la génération de l'URL: {e}")
            return ""

    def reset_changes(self) -> Tuple[bool, str]:
        """Annule toutes les modifications non commitées."""
        if not self.repo:
            return False, "❌ Dépôt non initialisé"
        
        try:
            self.repo.git.checkout("--", ".")
            self.repo.git.clean("-fd")
            return True, "✅ Modifications annulées"
        except GitCommandError as e:
            return False, f"❌ Erreur: {str(e)}"
