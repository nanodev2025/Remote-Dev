"""
AI Handler - Transforme les instructions en modifications de fichiers
Supporte plusieurs providers IA : Gemini (Google), Groq, OpenAI, Anthropic (Claude), Ollama (local)
"""

import os
import json
import logging
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class AIProvider(Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GROQ = "groq"
    OLLAMA = "ollama"
    GEMINI = "gemini"


@dataclass
class FileOperation:
    """Représente une opération sur un fichier."""
    action: str  # "create", "modify", "delete"
    file_path: str
    content: Optional[str] = None
    description: str = ""


@dataclass
class AIResponse:
    """Réponse structurée de l'IA."""
    success: bool
    operations: List[FileOperation]
    explanation: str
    error: Optional[str] = None


class AIHandler:
    """Gère les appels à l'API IA pour interpréter les instructions."""

    SYSTEM_PROMPT = """Tu es un assistant de développement expert. Tu reçois des instructions en langage naturel et tu dois les transformer en opérations concrètes sur des fichiers de code.

Tu travailles sur un projet Python situé dans le répertoire de travail. Voici la structure actuelle des fichiers que tu peux modifier.

RÈGLES IMPORTANTES:
1. Réponds UNIQUEMENT en JSON valide
2. Ne modifie que les fichiers nécessaires
3. Fournis le contenu COMPLET des fichiers modifiés ou créés
4. Sois précis et concis dans tes explications

FORMAT DE RÉPONSE JSON:
{
    "success": true,
    "explanation": "Description courte de ce qui a été fait",
    "operations": [
        {
            "action": "create|modify|delete",
            "file_path": "chemin/relatif/fichier.py",
            "content": "contenu complet du fichier si create ou modify",
            "description": "description de l'opération"
        }
    ]
}

EXEMPLES D'ACTIONS:
- "create": Créer un nouveau fichier
- "modify": Modifier un fichier existant (fournir le contenu complet)
- "delete": Supprimer un fichier

Si l'instruction n'est pas claire ou impossible à réaliser, réponds avec:
{
    "success": false,
    "explanation": "Explication du problème",
    "operations": [],
    "error": "Description de l'erreur"
}
"""

    def __init__(self, provider: str = "gemini", workspace_path: str = "."):
        """
        Initialise le handler IA.
        
        Args:
            provider: "gemini", "groq", "openai", "anthropic" ou "ollama"
            workspace_path: Chemin vers le répertoire de travail
        """
        self.provider = AIProvider(provider.lower())
        self.workspace_path = workspace_path
        self.client = None
        self._init_client()

    def _init_client(self) -> None:
        """Initialise le client API selon le provider."""
        if self.provider == AIProvider.ANTHROPIC:
            from anthropic import Anthropic
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY non définie")
            self.client = Anthropic(api_key=api_key)
            self.model = "claude-sonnet-4-20250514"
            logger.info("✅ Client Anthropic initialisé")
            
        elif self.provider == AIProvider.OPENAI:
            from openai import OpenAI
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY non définie")
            self.client = OpenAI(api_key=api_key)
            self.model = "gpt-4o"
            logger.info("✅ Client OpenAI initialisé")
        
        elif self.provider == AIProvider.GROQ:
            from openai import OpenAI
            api_key = os.getenv("GROQ_API_KEY")
            if not api_key:
                raise ValueError("GROQ_API_KEY non définie")
            self.client = OpenAI(
                api_key=api_key,
                base_url="https://api.groq.com/openai/v1"
            )
            self.model = "llama-3.3-70b-versatile"
            logger.info("✅ Client Groq initialisé (gratuit!)")
        
        elif self.provider == AIProvider.OLLAMA:
            from openai import OpenAI
            self.client = OpenAI(
                api_key="ollama",  # Ollama n'a pas besoin de clé
                base_url=os.getenv("OLLAMA_URL", "http://localhost:11434/v1")
            )
            self.model = os.getenv("OLLAMA_MODEL", "llama3.2")
            logger.info(f"✅ Client Ollama initialisé (modèle: {self.model})")
        
        elif self.provider == AIProvider.GEMINI:
            import google.generativeai as genai
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                raise ValueError("GEMINI_API_KEY non définie")
            genai.configure(api_key=api_key)
            # Important: certains modèles ont un quota gratuit à 0 selon les comptes.
            # `models/gemini-flash-lite-latest` est généralement disponible en "free tier".
            model_name = os.getenv("GEMINI_MODEL", "models/gemini-flash-lite-latest")
            self.client = genai.GenerativeModel(model_name)
            self.model = model_name
            logger.info(f"✅ Client Google Gemini initialisé (modèle: {self.model})")

    def _get_workspace_structure(self) -> str:
        """Retourne la structure des fichiers du workspace."""
        structure = []
        
        for root, dirs, files in os.walk(self.workspace_path):
            # Ignorer les dossiers cachés et node_modules, venv, etc.
            dirs[:] = [d for d in dirs if not d.startswith('.') 
                       and d not in ['node_modules', 'venv', '__pycache__', '.git']]
            
            level = root.replace(self.workspace_path, '').count(os.sep)
            indent = '  ' * level
            folder_name = os.path.basename(root) or '.'
            structure.append(f"{indent}📁 {folder_name}/")
            
            sub_indent = '  ' * (level + 1)
            for file in files:
                if not file.startswith('.'):
                    structure.append(f"{sub_indent}📄 {file}")
        
        return '\n'.join(structure) if structure else "Répertoire vide"

    def _get_file_content(self, file_path: str) -> Optional[str]:
        """Lit le contenu d'un fichier."""
        full_path = os.path.join(self.workspace_path, file_path)
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return None
        except Exception as e:
            logger.error(f"Erreur lecture {file_path}: {e}")
            return None

    def _build_context(self, instruction: str, relevant_files: List[str] = None) -> str:
        """Construit le contexte pour l'IA."""
        context_parts = [
            f"📂 STRUCTURE DU PROJET:\n{self._get_workspace_structure()}",
            f"\n📝 INSTRUCTION:\n{instruction}"
        ]
        
        # Ajouter le contenu des fichiers pertinents
        if relevant_files:
            for file_path in relevant_files:
                content = self._get_file_content(file_path)
                if content:
                    context_parts.append(f"\n📄 FICHIER {file_path}:\n```\n{content}\n```")
        
        return "\n".join(context_parts)

    async def process_instruction(
        self, 
        instruction: str, 
        relevant_files: List[str] = None
    ) -> AIResponse:
        """
        Traite une instruction et retourne les opérations à effectuer.
        
        Args:
            instruction: L'instruction en langage naturel
            relevant_files: Liste des fichiers à inclure dans le contexte
            
        Returns:
            AIResponse contenant les opérations à effectuer
        """
        context = self._build_context(instruction, relevant_files or [])
        
        try:
            if self.provider == AIProvider.ANTHROPIC:
                response = await self._call_anthropic(context)
            elif self.provider == AIProvider.GEMINI:
                response = await self._call_gemini(context)
            else:
                # OpenAI, Groq et Ollama utilisent le même format
                response = await self._call_openai(context)
            
            return self._parse_response(response)
            
        except Exception as e:
            logger.error(f"Erreur IA: {e}")
            return AIResponse(
                success=False,
                operations=[],
                explanation="",
                error=str(e)
            )

    async def _call_anthropic(self, context: str) -> str:
        """Appelle l'API Anthropic."""
        import asyncio
        
        def sync_call():
            message = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                system=self.SYSTEM_PROMPT,
                messages=[
                    {"role": "user", "content": context}
                ]
            )
            return message.content[0].text
        
        return await asyncio.get_event_loop().run_in_executor(None, sync_call)

    async def _call_openai(self, context: str) -> str:
        """Appelle l'API OpenAI."""
        import asyncio
        
        def sync_call():
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.SYSTEM_PROMPT},
                    {"role": "user", "content": context}
                ],
                max_tokens=4096,
                response_format={"type": "json_object"}
            )
            return response.choices[0].message.content
        
        return await asyncio.get_event_loop().run_in_executor(None, sync_call)

    async def _call_gemini(self, context: str) -> str:
        """Appelle l'API Google Gemini."""
        import asyncio
        try:
            # google.api_core n'est pas toujours présent selon les versions
            from google.api_core.exceptions import ResourceExhausted  # type: ignore
        except Exception:  # pragma: no cover
            ResourceExhausted = None  # type: ignore
        
        full_prompt = f"{self.SYSTEM_PROMPT}\n\n{context}"
        max_out = int(os.getenv("AI_MAX_OUTPUT_TOKENS", "2048"))
        
        def sync_call():
            try:
                response = self.client.generate_content(
                    full_prompt,
                    generation_config={
                        "response_mime_type": "application/json",
                        "max_output_tokens": max_out,
                    },
                )

                # `response.text` peut échouer selon finish_reason, on tente une extraction robuste.
                try:
                    return response.text
                except Exception:
                    candidates = getattr(response, "candidates", None) or []
                    if candidates:
                        content = getattr(candidates[0], "content", None)
                        parts = getattr(content, "parts", None) or []
                        if parts and hasattr(parts[0], "text"):
                            return parts[0].text
                    raise
            except Exception as e:
                msg = str(e)
                # Message plus actionnable en cas de quota
                if (ResourceExhausted and isinstance(e, ResourceExhausted)) or ("Quota exceeded" in msg) or ("ResourceExhausted" in msg) or ("429" in msg):
                    raise RuntimeError(
                        "Quota Gemini dépassé. Essaie un modèle compatible free-tier via `GEMINI_MODEL=models/gemini-flash-lite-latest` "
                        "ou active la facturation sur ton projet Google Cloud."
                    ) from e
                raise
        
        return await asyncio.get_event_loop().run_in_executor(None, sync_call)

    def _parse_response(self, response_text: str) -> AIResponse:
        """Parse la réponse JSON de l'IA."""
        try:
            # Nettoyer la réponse si nécessaire
            response_text = response_text.strip()
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            
            data = json.loads(response_text.strip())
            
            operations = []
            for op in data.get("operations", []):
                operations.append(FileOperation(
                    action=op.get("action", "modify"),
                    file_path=op.get("file_path", ""),
                    content=op.get("content"),
                    description=op.get("description", "")
                ))
            
            return AIResponse(
                success=data.get("success", False),
                operations=operations,
                explanation=data.get("explanation", ""),
                error=data.get("error")
            )
            
        except json.JSONDecodeError as e:
            logger.error(f"Erreur parsing JSON: {e}")
            return AIResponse(
                success=False,
                operations=[],
                explanation="",
                error=f"Erreur de parsing: {str(e)}\nRéponse: {response_text[:200]}"
            )

    def apply_operations(self, operations: List[FileOperation]) -> List[Dict[str, Any]]:
        """
        Applique les opérations sur les fichiers.
        
        Args:
            operations: Liste des opérations à appliquer
            
        Returns:
            Liste des résultats pour chaque opération
        """
        results = []
        
        for op in operations:
            result = {"file": op.file_path, "action": op.action, "success": False, "error": None}
            full_path = os.path.join(self.workspace_path, op.file_path)
            
            try:
                if op.action == "delete":
                    if os.path.exists(full_path):
                        os.remove(full_path)
                        result["success"] = True
                        logger.info(f"🗑️ Supprimé: {op.file_path}")
                    else:
                        result["error"] = "Fichier non trouvé"
                        
                elif op.action in ["create", "modify"]:
                    # Créer les dossiers parents si nécessaire
                    os.makedirs(os.path.dirname(full_path), exist_ok=True)
                    
                    with open(full_path, 'w', encoding='utf-8') as f:
                        f.write(op.content or "")
                    
                    result["success"] = True
                    emoji = "📝" if op.action == "modify" else "✨"
                    logger.info(f"{emoji} {op.action.capitalize()}: {op.file_path}")
                    
                else:
                    result["error"] = f"Action inconnue: {op.action}"
                    
            except Exception as e:
                result["error"] = str(e)
                logger.error(f"❌ Erreur {op.action} {op.file_path}: {e}")
            
            results.append(result)
        
        return results

    def rollback_operations(self, operations: List[FileOperation]) -> None:
        """
        Annule les opérations en cas d'erreur.
        Supprime les fichiers créés, restaure les fichiers modifiés via git.
        """
        for op in operations:
            full_path = os.path.join(self.workspace_path, op.file_path)
            
            if op.action == "create" and os.path.exists(full_path):
                try:
                    os.remove(full_path)
                    logger.info(f"↩️ Rollback: suppression de {op.file_path}")
                except Exception as e:
                    logger.error(f"Erreur rollback {op.file_path}: {e}")
