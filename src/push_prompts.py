"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
2. Valida os prompts
3. Faz push PÚBLICO para o LangSmith Hub
4. Adiciona metadados (tags, descrição, técnicas utilizadas)

SIMPLIFICADO: Código mais limpo e direto ao ponto.
"""

import os
import sys
from dotenv import load_dotenv
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
from utils import load_yaml, check_env_vars, print_section_header

load_dotenv()


def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    """
    Faz push do prompt otimizado para o LangSmith Hub (PÚBLICO).

    Args:
        prompt_name: Nome do prompt
        prompt_data: Dados do prompt

    Returns:
        True se sucesso, False caso contrário
    """
    try:
        root_key = list(prompt_data.keys())[0]
        data = prompt_data[root_key]
        
        system_prompt = data.get("system_prompt", "")
        user_prompt = data.get("user_prompt", "")
        
        # Cria ChatPromptTemplate com system + user messages
        template = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", user_prompt)
        ])
        
        # Monta link público
        print(f"Subindo prompt: {prompt_name}...")
        
        hub.push(
            prompt_name,
            template,
            new_repo_description=data.get("description", ""),
            new_repo_is_public=True
        )
        print(f"✓ Prompt '{prompt_name}' publicado com sucesso no LangSmith!")
        return True
    except Exception as e:
        print(f"❌ Erro ao fazer push do prompt: {e}")
        return False


def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    """
    Valida estrutura básica de um prompt (versão simplificada).

    Args:
        prompt_data: Dados do prompt

    Returns:
        (is_valid, errors) - Tupla com status e lista de erros
    """
    from utils import validate_prompt_structure
    
    if not prompt_data or not isinstance(prompt_data, dict):
        return False, ["Arquivo vazio ou mal formatado"]
        
    root_key = list(prompt_data.keys())[0]
    data = prompt_data[root_key]
    
    return validate_prompt_structure(data)


def main():
    """Função principal"""
    print_section_header("PUSH PROMPTS PARA O LANGSMITH")
    
    required_vars = ["LANGSMITH_API_KEY", "USERNAME_LANGSMITH_HUB"]
    if not check_env_vars(required_vars):
        return 1
        
    username = os.getenv("USERNAME_LANGSMITH_HUB")
    prompt_file = "prompts/bug_to_user_story_v2.yml"
    
    print(f"Lendo {prompt_file}...")
    prompt_data = load_yaml(prompt_file)
    
    if not prompt_data:
        return 1
        
    is_valid, errors = validate_prompt(prompt_data)
    if not is_valid:
        print("❌ Validação do prompt falhou:")
        for error in errors:
            print(f"  - {error}")
        return 1
        
    prompt_name = f"{username}/bug_to_user_story_v2"
    success = push_prompt_to_langsmith(prompt_name, prompt_data)
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
