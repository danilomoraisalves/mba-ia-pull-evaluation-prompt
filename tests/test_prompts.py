"""
Testes automatizados para validação de prompts.
"""
import pytest
import yaml
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils import validate_prompt_structure

def load_prompts(file_path: str):
    """Carrega prompts do arquivo YAML."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

class TestPrompts:
    def test_prompt_has_system_prompt(self):
        """Verifica se o campo 'system_prompt' existe e não está vazio."""
        prompt_data = load_prompts("prompts/bug_to_user_story_v2.yml")
        root_key = list(prompt_data.keys())[0]
        assert "system_prompt" in prompt_data[root_key], "O campo system_prompt não existe"
        assert prompt_data[root_key]["system_prompt"].strip() != "", "O campo system_prompt está vazio"

    def test_prompt_has_role_definition(self):
        """Verifica se o prompt define uma persona (ex: "Você é um Product Manager")."""
        prompt_data = load_prompts("prompts/bug_to_user_story_v2.yml")
        root_key = list(prompt_data.keys())[0]
        sys_prompt = prompt_data[root_key]["system_prompt"].lower()
        # Verifica se usa você é ou atue como
        assert "você é" in sys_prompt or "atue como" in sys_prompt or "product manager" in sys_prompt, "Persona não definida claramente no system_prompt"

    def test_prompt_mentions_format(self):
        """Verifica se o prompt exige formato Markdown ou User Story padrão."""
        prompt_data = load_prompts("prompts/bug_to_user_story_v2.yml")
        root_key = list(prompt_data.keys())[0]
        sys_prompt = prompt_data[root_key]["system_prompt"].lower()
        assert "markdown" in sys_prompt or "user story" in sys_prompt or "formato" in sys_prompt, "O prompt não exige um formato claro"

    def test_prompt_has_few_shot_examples(self):
        """Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot)."""
        prompt_data = load_prompts("prompts/bug_to_user_story_v2.yml")
        root_key = list(prompt_data.keys())[0]
        sys_prompt = prompt_data[root_key]["system_prompt"].lower()
        assert "exemplo" in sys_prompt or "example" in sys_prompt, "Não foram encontrados exemplos (Few-shot) no prompt"

    def test_prompt_no_todos(self):
        """Garante que você não esqueceu nenhum `[TODO]` no texto."""
        prompt_data = load_prompts("prompts/bug_to_user_story_v2.yml")
        root_key = list(prompt_data.keys())[0]
        sys_prompt = prompt_data[root_key]["system_prompt"]
        assert "TODO" not in sys_prompt, "Foi encontrado a marcação TODO no system_prompt, favor preencher"

    def test_minimum_techniques(self):
        """Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas."""
        prompt_data = load_prompts("prompts/bug_to_user_story_v2.yml")
        root_key = list(prompt_data.keys())[0]
        techniques = prompt_data[root_key].get("techniques_applied", [])
        assert len(techniques) >= 2, "Menos de 2 técnicas listadas nos metadados"

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])