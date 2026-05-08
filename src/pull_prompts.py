"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull dos prompts do Hub
3. Salva localmente em prompts/bug_to_user_story_v1.yml

SIMPLIFICADO: Usa serialização nativa do LangChain para extrair prompts.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from langchain import hub
from utils import save_yaml, check_env_vars, print_section_header

load_dotenv()


def pull_prompts_from_langsmith():
    print("Puxando prompt base (v1)...")
    try:
        prompt = hub.pull("leonanluppi/bug_to_user_story_v1")
        
        # O prompt_v1 tem formato específico, precisamos extrair os dados.
        # Caso o pull retorne um objecto MessagePromptTemplate etc, nós guardamos o yaml
        prompt_data = {
            "bug_to_user_story_v1": {
                "description": "Prompt para converter relatos de bugs em User Stories",
                "system_prompt": prompt.messages[0].prompt.template if hasattr(prompt, "messages") and len(prompt.messages) > 0 else "Você é um assistente...",
                "user_prompt": prompt.messages[1].prompt.template if hasattr(prompt, "messages") and len(prompt.messages) > 1 else "{bug_report}",
                "version": "v1",
                "created_at": "2025-01-15",
                "tags": ["bug-analysis", "user-story", "product-management"]
            }
        }
        
        save_yaml(prompt_data, "prompts/bug_to_user_story_v1.yml")
        print("✓ Prompt v1 salvo em prompts/bug_to_user_story_v1.yml")
        return True
    except Exception as e:
        print(f"❌ Erro ao puxar prompt: {e}")
        return False


def main():
    """Função principal"""
    print_section_header("PULL PROMPTS DO LANGSMITH")
    
    required_vars = ["LANGSMITH_API_KEY", "LANGSMITH_PROJECT"]
    if not check_env_vars(required_vars):
        return 1
        
    success = pull_prompts_from_langsmith()
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
