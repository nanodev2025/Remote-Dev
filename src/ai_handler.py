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

    SYSTEM_PROMPT = """Tu es un assistant de développement expert et expérimenté. Tu reçois des instructions en langage naturel et tu dois les transformer en opérations concrètes et de qualité sur des fichiers de code.

Tu travailles sur un projet situé dans le répertoire de travail. Tu as accès à la structure complète des fichiers et tu peux les modifier, créer ou supprimer.

🎯 TON RÔLE:
- Analyser attentivement chaque instruction
- Comprendre le contexte et les besoins réels
- Produire du code de qualité, propre et bien structuré
- Suivre les meilleures pratiques du langage utilisé
- Ajouter des commentaires pertinents quand nécessaire
- Gérer les erreurs et cas limites

📋 RÈGLES CRITIQUES:
1. Réponds UNIQUEMENT en JSON valide (pas de markdown, pas de texte avant/après)
2. Ne modifie que les fichiers strictement nécessaires
3. Fournis le contenu COMPLET des fichiers modifiés ou créés (pas juste les changements)
4. Sois précis, détaillé et professionnel dans tes explications
5. Respecte le style de code existant si tu modifies un fichier
6. Assure-toi que le code est fonctionnel et sans erreurs de syntaxe
7. Pour les sites web, crée une structure complète et moderne (HTML, CSS, JS si nécessaire)

🚨 RÈGLE ABSOLUE POUR LES CHEMINS DE FICHIERS:
- Les chemins doivent TOUJOURS commencer directement par le nom du fichier ou un sous-dossier (ex: "index.html", "style.css", "src/app.py")
- JAMAIS inclure le nom du dossier parent du workspace dans le chemin
- Exemples CORRECTS: "index.html", "style.css", "src/main.js", "assets/logo.png"
- Exemples INCORRECTS: "remotecode/index.html", "remotecode/style.css", "remotecode/remotecode/index.html"
- Si tu vois un chemin qui commence par le nom du workspace, supprime ce préfixe

📝 FORMAT DE RÉPONSE JSON (STRICT):
{
    "success": true,
    "explanation": "Description détaillée et claire de ce qui a été fait, pourquoi, et comment l'utiliser",
    "operations": [
        {
            "action": "create|modify|delete",
            "file_path": "chemin/relatif/fichier.ext",
            "content": "contenu COMPLET du fichier si create ou modify (avec toutes les balises, imports, etc.)",
            "description": "description précise de l'opération effectuée"
        }
    ]
}

🔧 EXEMPLES D'ACTIONS:
- "create": Créer un nouveau fichier avec tout son contenu complet
- "modify": Modifier un fichier existant (fournir le contenu COMPLET du fichier modifié, pas juste les changements)
- "delete": Supprimer un fichier

⚠️ EN CAS D'ERREUR:
{
    "success": false,
    "explanation": "Explication détaillée du problème rencontré",
    "operations": [],
    "error": "Description précise de l'erreur et suggestions pour la résoudre"
}

💡 CONSEILS POUR UN BON CODE:
- Code propre et lisible
- Nommage explicite et cohérent
- Structure logique et organisée
- Gestion d'erreurs appropriée
- Documentation/commentaires utiles
- Respect des conventions du langage
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
            # Utiliser le meilleur modèle disponible (llama-3.1-70b-versatile est plus récent et performant)
            self.model = os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile")
            logger.info(f"✅ Client Groq initialisé (modèle: {self.model})")
        
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
        workspace_name = os.path.basename(os.path.abspath(self.workspace_path))
        context_parts = [
            f"📂 STRUCTURE DU PROJET (répertoire de travail: {workspace_name}):\n{self._get_workspace_structure()}",
            f"\n📝 INSTRUCTION UTILISATEUR:\n{instruction}",
            f"\n🚨 RÈGLE ABSOLUE POUR LES CHEMINS DE FICHIERS:",
            f"- Les chemins doivent TOUJOURS commencer directement par le nom du fichier ou un sous-dossier",
            f"- Exemples CORRECTS: 'index.html', 'style.css', 'src/app.py', 'assets/logo.png'",
            f"- Exemples INCORRECTS (À ÉVITER): '{workspace_name}/index.html', '{workspace_name}/{workspace_name}/index.html'",
            f"- Si tu vois '{workspace_name}' dans un chemin, supprime ce préfixe complètement",
            f"- Les fichiers doivent être créés/modifiés directement à la racine du workspace ou dans des sous-dossiers normaux",
            f"\n💡 AUTRES INSTRUCTIONS:",
            f"- Analyse bien l'instruction, comprends ce qui est demandé, et produit un code de qualité professionnelle."
        ]
        
        # Ajouter le contenu des fichiers pertinents
        if relevant_files:
            context_parts.append(f"\n📄 FICHIERS PERTINENTS À CONSIDÉRER:")
            for file_path in relevant_files:
                content = self._get_file_content(file_path)
                if content:
                    context_parts.append(f"\n📄 {file_path}:\n```\n{content}\n```")
                else:
                    context_parts.append(f"\n⚠️ {file_path}: fichier non trouvé")
        else:
            # Si aucun fichier spécifique, inclure les fichiers principaux du projet
            main_files = self._find_main_files()
            if main_files:
                context_parts.append(f"\n📄 FICHIERS PRINCIPAUX DU PROJET:")
                for file_path in main_files[:5]:  # Limiter à 5 fichiers pour ne pas surcharger
                    content = self._get_file_content(file_path)
                    if content:
                        # Limiter la taille du contenu pour ne pas dépasser les limites
                        if len(content) > 2000:
                            content = content[:2000] + "\n... (tronqué)"
                        context_parts.append(f"\n📄 {file_path}:\n```\n{content}\n```")
        
        return "\n".join(context_parts)
    
    def _find_main_files(self) -> List[str]:
        """Trouve les fichiers principaux du projet (index.html, main.py, app.py, etc.)."""
        main_patterns = [
            "index.html", "index.js", "index.jsx", "index.ts", "index.tsx",
            "main.py", "app.py", "main.js", "app.js", "App.jsx", "App.tsx",
            "package.json", "requirements.txt", "README.md"
        ]
        
        found_files = []
        for root, dirs, files in os.walk(self.workspace_path):
            # Ignorer les dossiers cachés et dépendances
            if any(skip in root for skip in ['.git', 'node_modules', 'venv', '__pycache__', '.']):
                continue
            
            for file in files:
                if file in main_patterns:
                    rel_path = os.path.relpath(os.path.join(root, file), self.workspace_path)
                    found_files.append(rel_path)
        
        return found_files

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
        """Appelle l'API OpenAI (utilisé aussi pour Groq et Ollama)."""
        import asyncio
        
        # Paramètres améliorés pour de meilleurs résultats
        temperature = float(os.getenv("AI_TEMPERATURE", "0.7"))  # 0.7 = équilibre créativité/précision
        max_tokens = int(os.getenv("AI_MAX_OUTPUT_TOKENS", "8192"))  # Plus de tokens pour des réponses complètes
        
        def sync_call():
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.SYSTEM_PROMPT},
                    {"role": "user", "content": context}
                ],
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=0.9,  # Nucleus sampling pour plus de diversité
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
        max_out = int(os.getenv("AI_MAX_OUTPUT_TOKENS", "8192"))  # Plus de tokens pour Gemini aussi
        temperature = float(os.getenv("AI_TEMPERATURE", "0.7"))
        
        def sync_call():
            try:
                response = self.client.generate_content(
                    full_prompt,
                    generation_config={
                        "response_mime_type": "application/json",
                        "max_output_tokens": max_out,
                        "temperature": temperature,  # Ajouter température pour Gemini
                        "top_p": 0.9,
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

    def _normalize_file_path(self, file_path: str) -> str:
        """
        Normalise le chemin du fichier pour éviter les sous-dossiers récursifs.
        Supprime les préfixes qui correspondent au nom du workspace.
        
        Args:
            file_path: Chemin du fichier à normaliser
            
        Returns:
            Chemin normalisé
        """
        workspace_name = os.path.basename(os.path.abspath(self.workspace_path))
        
        # Nettoyer le chemin
        path = file_path.strip()
        
        # Supprimer les préfixes répétitifs du nom du workspace
        # Ex: "remotecode/remotecode/index.html" -> "index.html"
        # Ex: "remotecode/index.html" -> "index.html"
        while path.startswith(f"{workspace_name}/"):
            path = path[len(f"{workspace_name}/"):]
        
        # Supprimer les slashes en début de chemin
        path = path.lstrip("/")
        
        # Si le chemin est vide après nettoyage, utiliser juste le nom du fichier
        if not path or path == workspace_name:
            # Extraire le nom du fichier si possible
            original_path = file_path.strip().lstrip("/")
            if "/" in original_path:
                path = "/".join(original_path.split("/")[-2:])  # Garder au plus 2 niveaux
            else:
                path = original_path
        
        return path

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
            # Normaliser le chemin pour éviter les sous-dossiers récursifs
            normalized_path = self._normalize_file_path(op.file_path)
            
            result = {"file": normalized_path, "action": op.action, "success": False, "error": None}
            full_path = os.path.join(self.workspace_path, normalized_path)
            
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
