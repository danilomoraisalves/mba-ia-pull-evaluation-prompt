# Pull, Otimização e Avaliação de Prompts com LangChain e LangSmith

---

## Técnicas Aplicadas (Fase 2)

### 1. Role Prompting

**Técnica:** Definir uma persona detalhada e específica no system prompt antes de qualquer instrução.

**Justificativa:** Quando o modelo tem um papel claro, ele produz saídas mais coerentes com o vocabulário e as expectativas do domínio. Sem persona, o modelo tende a respostas vagas e genéricas.

**Como apliquei:**
```
Você é um Product Manager Sênior, especialista em refinamento de backlog,
trabalhando lado a lado com um Arquiteto de Software. Sua missão é converter
relatos de bugs em User Stories acionáveis, com a profundidade EXATA exigida
pela complexidade do bug — nem mais, nem menos.
```

---

### 2. Few-shot Learning

**Técnica:** Fornecer exemplos concretos de entrada → saída no system prompt antes do input real.

**Justificativa:** É a técnica de maior impacto para tarefas de transformação de formato. Com exemplos reais, o modelo aprende o padrão exato de saída esperado sem especificações longas.

**Como apliquei:** 7 exemplos no system prompt cobrindo todos os perfis do dataset:

| Exemplo | Tipo | Cobertura |
|---|---|---|
| 1 | SIMPLES | Bug de botão — formato mínimo com 5 bullets |
| 1b | SIMPLES | Bug de navegador específico (Safari) |
| 1c | SIMPLES | Dado incorreto (contagem errada) |
| 1d | SIMPLES | Validação de formulário com mensagem de formato |
| 2 | MÉDIO | Performance SQL — critérios + contexto técnico |
| 2b | MÉDIO | Mobile/Android — `Critérios Técnicos` + `Contexto do Bug` |
| 3 | SEGURANÇA | Múltiplos papéis (usuário vs admin) + OWASP |
| 4 | COMPLEXO | Formato completo com 6 seções nomeadas |

---

### 3. Chain of Thought (CoT)

**Técnica:** Instruir o modelo a raciocinar passo a passo (mentalmente) antes de produzir a saída.

**Justificativa:** A tarefa exige classificar a complexidade do bug (SIMPLES / MÉDIO / COMPLEXO) antes de escolher o formato de saída. Sem CoT, o modelo escolhe formato aleatório e produz saídas desproporcionais.

**Como apliquei:**
```
# ETAPA 1 — RACIOCÍNIO (Chain of Thought, NÃO escreva isso na resposta)
Antes de escrever a User Story, pense passo a passo (silenciosamente):
1. Classifique a COMPLEXIDADE do bug: SIMPLES / MÉDIO / COMPLEXO
2. Identifique o ATOR real (cliente, vendedor, admin, "o sistema"...)
3. Liste APENAS os fatos presentes no relato — não invente dados
```

---

### 4. Skeleton of Thought

**Técnica:** Definir previamente os "ossos" da resposta (estrutura de seções/formatos) antes de preenchê-los.

**Justificativa:** Evita que o modelo invente estruturas próprias inconsistentes entre execuções. Cada nível de complexidade tem um template fixo e nomeado.

**Como apliquei:** Três templates de saída documentados no system prompt:
- `[FORMATO SIMPLES]` — apenas 5 bullets Dado/Quando/Então/E/E
- `[FORMATO MÉDIO]` — critérios + 1-2 seções de contexto técnico
- `[FORMATO COMPLEXO]` — 6 seções nomeadas com `===`

---

### 5. Conditional Output Formatting

**Técnica:** Regras condicionais explícitas que mapeiam tipo de entrada → tipo de saída.

**Justificativa:** Permite que um único prompt trate bugs de complexidades muito diferentes sem degradar nenhum dos casos. Sem isso, o modelo usava sempre o formato complexo mesmo para bugs de 1 linha.

**Como apliquei:** Critérios objetivos de classificação no system prompt:
```
- SIMPLES: relato curto (1-2 frases), 1 sintoma, sem detalhes técnicos
- MÉDIO: relato com steps to reproduce, logs ou 1 detalhe técnico
- COMPLEXO: relato longo com MÚLTIPLOS problemas numerados (1., 2., 3.),
  seções em CAPS, métricas de negócio explícitas (NPS, churn, R$)
```

---

## Resultados Finais

### Resultado aprovado (v2.10)

```
==================================================
Prompt: danilo-prompts/bug_to_user_story_v2
==================================================

Métricas Derivadas:
  - Helpfulness: 0.97 ✓
  - Correctness: 0.94 ✓

Métricas Base:
  - F1-Score: 0.91 ✓
  - Clarity: 0.96 ✓
  - Precision: 0.97 ✓

--------------------------------------------------
📊 MÉDIA GERAL: 0.9484
--------------------------------------------------

✅ STATUS: APROVADO - Todas as métricas >= 0.9
```

### Tabela comparativa: v1 (ruim) vs v2 (otimizado)

| Métrica | v1 (baseline) | v2.10 (otimizado) | Melhoria |
|---|---|---|---|
| Helpfulness | ~0.45 | **0.97** | +0.52 |
| Correctness | ~0.52 | **0.94** | +0.42 |
| F1-Score | ~0.48 | **0.91** | +0.43 |
| Clarity | ~0.50 | **0.96** | +0.46 |
| Precision | ~0.46 | **0.97** | +0.51 |
| **Média** | **~0.48** | **0.9484** | **+0.47** |

### Histórico de iterações

| Versão | F1 | Clarity | Precision | Helpfulness | Correctness | Média | Status |
|---|---|---|---|---|---|---|---|
| v2.3 | 0.86 | 0.91 | 0.90 | 0.91 | 0.88 | 0.892 | ❌ |
| v2.4 | 0.84 | 0.94 | 0.95 | 0.95 | 0.90 | 0.916 | ❌ |
| v2.5 | 0.86 | 0.95 | 0.95 | 0.95 | 0.91 | 0.924 | ❌ |
| v2.6 | 0.83 | 0.96 | 0.96 | 0.96 | 0.90 | 0.922 | ❌ |
| v2.7 | 0.89 | 0.96 | 0.96 | 0.96 | 0.93 | 0.939 | ❌ |
| v2.8 | 0.85 | 0.96 | 0.96 | 0.96 | 0.91 | 0.929 | ❌ |
| v2.9 | 0.87 | 0.98 | 0.96 | 0.97 | 0.92 | 0.939 | ❌ |
| **v2.10** | **0.91** | **0.96** | **0.97** | **0.97** | **0.94** | **0.948** | **✅** |

### Evidências no LangSmith

- **Prompt público:** https://smith.langchain.com/hub/danilo-prompts/bug_to_user_story_v2
- **Dashboard do projeto:** https://smith.langchain.com/public/bf2303ca-fdbf-4706-8cce-70ac3bd2eb77/d
- **Trace público 1:** https://smith.langchain.com/public/76c55499-8647-4998-bbf7-f8ba771f9daa/r
- **Trace público 2:** https://smith.langchain.com/public/2778f9de-fe7b-417a-88d9-679b3aac3e2e/r
- **Trace público 3:** https://smith.langchain.com/public/5d2484e0-4a86-435c-9db8-0099faa9df9c/r
- **Print das avaliações:** [docs/print-avaliacao.png](docs/print-avaliacao.png)

---

## Como Executar

### Pré-requisitos

- Python 3.9+
- Conta no [LangSmith](https://smith.langchain.com/) com API Key
- API Key do [Google Gemini](https://aistudio.google.com/app/apikey) (gratuito, 1500 req/dia) **ou** [OpenAI](https://platform.openai.com/api-keys)

### Instalação

```bash
git clone https://github.com/danilomoraisalves/mba-ia-pull-evaluation-prompt
cd mba-ia-pull-evaluation-prompt

python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Configuração do `.env`

```bash
cp .env.example .env
```

Preencha com suas credenciais:

```env
# LangSmith
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_API_KEY=ls__...
LANGSMITH_PROJECT=prompt-optimization
USERNAME_LANGSMITH_HUB=danilo-prompts

# Google Gemini (gratuito)
GOOGLE_API_KEY=AIza...
LLM_PROVIDER=google
LLM_MODEL=gemini-2.5-flash
EVAL_MODEL=gemini-2.5-flash
```

### Fase 1 — Pull do prompt base (v1)

```bash
python src/pull_prompts.py
```

Salva o prompt original em `prompts/bug_to_user_story_v1.yml`.

### Fase 2 — Push do prompt otimizado (v2)

```bash
python src/push_prompts.py
```

Lê `prompts/bug_to_user_story_v2.yml` e publica em `danilo-prompts/bug_to_user_story_v2` no LangSmith Hub.

### Fase 3 — Avaliação

```bash
python src/evaluate.py
```

Avalia os 15 exemplos do dataset e exibe as 5 métricas. Critério de aprovação: todas ≥ 0.9.

### Fase 4 — Testes de validação

```bash
pytest tests/test_prompts.py -v
```

Executa os 6 testes automatizados que validam a estrutura do prompt v2.
