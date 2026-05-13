# Inventário do Projeto — Skill_Presentation

> Gerado pelo Scout em 2026-05-11
> Escala de confiança: 🟢 CONFIRMADO | 🟡 INFERIDO | 🔴 LACUNA

---

## Visão Geral

| Atributo               | Valor                                         |
| ---------------------- | --------------------------------------------- |
| Nome do projeto        | Skill_Presentation (Gerador de Apresentações) |
| Linguagem principal    | Python 3.13+ 🟢                               |
| Framework principal    | Streamlit + LangChain 🟢                      |
| Gerenciador de pacotes | uv (pyproject.toml) 🟢                        |
| Banco de dados         | Nenhum (stateless) 🟢                         |
| Interface              | Streamlit (web) 🟢                            |

---

## Estrutura de Pastas

```
.
├── apps/
│   └── streamlit/                # Aplicação principal
│       ├── agents/               # Pipeline de agentes (nodes)
│       │   ├── __init__.py
│       │   ├── content_node.py   # Geração de conteúdo (GPT-4o)
│       │   ├── html_node.py      # Renderização HTML (determinístico)
│       │   ├── model_selector.py # Seleção de modelo por complexidade
│       │   ├── pptx_node.py      # Conversão HTML → PPTX
│       │   ├── prompt_loader.py  # Carregamento de prompts .md
│       │   ├── quality_standards.py # Padrões de qualidade
│       │   ├── research_node.py  # Pesquisa web (Tavily/DDG)
│       │   ├── state.py          # PresentationState TypedDict
│       │   ├── structure_node.py # Estruturação de slides (LLM)
│       │   └── validation_node.py # Validação de arquivos gerados
│       ├── app.py                # Interface principal (formulários)
│       ├── app_chat.py           # Interface chat (prompt livre)
│       ├── config.py             # Settings via dotenv + lru_cache
│       └── template_register.py  # Registro de templates corporativos
├── exports/                      # Apresentações geradas (runtime)
├── prompt/                       # System prompts dos agentes (.md)
│   ├── content_agent.md
│   ├── html_generator.md
│   ├── proposal_agent.md
│   └── structure_agent.md
├── templates/                    # Templates visuais corporativos
│   ├── registry.json             # Registro de templates disponíveis
│   ├── empresa-teste/            # Template: base.pptx + manifest.json
│   └── template-50anos/          # Template: base.pptx + manifest.json
├── main.py                       # Entry point placeholder
├── pyproject.toml                # Configuração do projeto (uv)
├── .env / .env.example           # Variáveis de ambiente
└── .gitignore
```

---

## Módulos Identificados

| Módulo      | Caminho                                              | Responsabilidade                                 |
| ----------- | ---------------------------------------------------- | ------------------------------------------------ |
| `pipeline`  | `apps/streamlit/agents/`                             | Pipeline de geração de apresentações (6 nodes)   |
| `ui-forms`  | `apps/streamlit/app.py`                              | Interface Streamlit com formulários estruturados |
| `ui-chat`   | `apps/streamlit/app_chat.py`                         | Interface Streamlit modo chat livre              |
| `templates` | `apps/streamlit/template_register.py` + `templates/` | Sistema de templates corporativos                |
| `prompts`   | `prompt/`                                            | System prompts dos agentes em Markdown           |
| `config`    | `apps/streamlit/config.py`                           | Configuração centralizada via .env               |

---

## Modos de Operação

1. **Apresentação Livre** — Usuário descreve tema, sistema pesquisa dados e gera apresentação completa
2. **Proposta de Projeto** — Formulário estruturado (problema, solução, escopo, investimento) → apresentação de proposta
3. **Chat** — Prompt livre, geração direta de HTML via LLM
4. **Gerenciar Templates** — Upload de .pptx, extração de cores/fontes/logo

---

## Pipeline de Geração (Nodes)

```
Research → Structure → Content → HTML → PPTX → Validation
   │           │          │        │       │        │
   │           │          │        │       │        └─ Determinístico
   │           │          │        │       └─ Determinístico (python-pptx)
   │           │          │        └─ Determinístico (template rendering)
   │           │          └─ GPT-4o (complex)
   │           └─ gpt-4o-mini (simple)
   └─ Tavily/DuckDuckGo (sem LLM)
```

---

## Entry Points

| Arquivo                      | Tipo        | Descrição                                   |
| ---------------------------- | ----------- | ------------------------------------------- |
| `apps/streamlit/app.py`      | app_entry   | Interface principal Streamlit (formulários) |
| `apps/streamlit/app_chat.py` | app_entry   | Interface chat Streamlit                    |
| `main.py`                    | placeholder | Hello world (não usado em produção)         |

---

## Configuração

| Arquivo                   | Propósito                         |
| ------------------------- | --------------------------------- |
| `.env.example`            | Template de variáveis de ambiente |
| `pyproject.toml`          | Metadados do projeto (uv)         |
| `templates/registry.json` | Registro de templates visuais     |

---

## CI/CD

Nenhum pipeline de CI/CD identificado. 🟡

---

## Docker

Nenhum Dockerfile ou docker-compose.yml encontrado neste projeto específico. 🟢
(Nota: os steering files mencionam Docker, mas referem-se ao projeto maior "Gerador de Relatórios Kiro", não a este subprojeto de apresentações.)

---

## Testes

Nenhum framework de testes identificado. Nenhum arquivo `*test*` ou `*spec*` encontrado. 🟢

---

## Exports Gerados (Runtime)

| Arquivo  | Formato                            |
| -------- | ---------------------------------- |
| `*.html` | Apresentações HTML standalone      |
| `*.pptx` | Apresentações PowerPoint editáveis |
