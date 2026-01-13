"""
Gestionnaire Git - Gère les opérations git (add, commit, push)
"""

import os
import logging
from typing import Optional, Tuple
from git import Repo, InvalidGitRepositoryError, GitCommandError

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
            if not self.repo.index.diff("HEAD"):
                return False, "⚠️ Aucun changement à commiter"
            
            commit = self.repo.index.commit(message)
            commit_hash = commit.hexsha[:8]
            logger.info(f"✅ Commit créé: {commit_hash}")
            return True, f"✅ Commit: {commit_hash}"
        except GitCommandError as e:
            logger.error(f"❌ Erreur lors du commit: {e}")
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
            origin = self.repo.remote("origin")
            push_info = origin.push(self.branch)
            
            for info in push_info:
                if info.flags & info.ERROR:
                    return False, f"❌ Erreur push: {info.summary}"
            
            logger.info(f"✅ Push réussi vers {self.branch}")
            return True, f"✅ Push vers origin/{self.branch} réussi"
        except GitCommandError as e:
            logger.error(f"❌ Erreur lors du push: {e}")
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
            commit_hash = self.repo.head.commit.hexsha
            # Nettoyer l'URL GitHub
            base_url = github_url.rstrip(".git").rstrip("/")
            return f"{base_url}/commit/{commit_hash}"
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
