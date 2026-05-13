# Dicionário de Dados — Skill_Presentation

> Gerado pelo Arqueólogo em 2026-05-11
> Escala de confiança: 🟢 CONFIRMADO | 🟡 INFERIDO | 🔴 LACUNA

---

## 1. PresentationState (TypedDict)

Fonte: `apps/streamlit/agents/state.py`
Estado principal passado entre todos os nodes do pipeline.

| Campo                 | Tipo                          | Obrigatório | Default               | Descrição                               |
| --------------------- | ----------------------------- | ----------- | --------------------- | --------------------------------------- |
| `tema`                | `str`                         | sim         | —                     | Tema da apresentação (input do usuário) |
| `publico`             | `str`                         | sim         | —                     | Público-alvo selecionado                |
| `tom`                 | `str`                         | sim         | —                     | Tom da apresentação                     |
| `num_slides`          | `int`                         | sim         | 12                    | Número de slides desejado (5-25)        |
| `template`            | `str`                         | sim         | "Padrão (dark theme)" | Nome do template visual                 |
| `formato_saida`       | `list[str]`                   | sim         | ["HTML", "PPTX"]      | Formatos de exportação                  |
| `incluir_referencias` | `bool`                        | sim         | True                  | Incluir slide de referências            |
| `incluir_agenda`      | `bool`                        | sim         | True                  | Incluir slide de agenda                 |
| `mode`                | `Literal["free", "proposal"]` | sim         | "free"                | Modo de geração                         |
| `research_queries`    | `list[str]`                   | não         | []                    | Queries geradas para pesquisa           |
| `research_results`    | `list[ResearchResult]`        | não         | []                    | Resultados da pesquisa web              |
| `selected_data`       | `list[ResearchResult]`        | não         | []                    | Top 5 resultados filtrados              |
| `slide_titles`        | `list[str]`                   | não         | []                    | Títulos dos slides                      |
| `slides`              | `list[SlideContent]`          | não         | []                    | Conteúdo completo dos slides            |
| `html_content`        | `str`                         | não         | ""                    | HTML gerado                             |
| `html_path`           | `str`                         | não         | ""                    | Caminho do arquivo HTML salvo           |
| `pptx_path`           | `str`                         | não         | ""                    | Caminho do arquivo PPTX salvo           |
| `is_valid`            | `bool`                        | não         | False                 | Resultado da validação                  |
| `error`               | `str`                         | não         | ""                    | Mensagem de erro (se houver)            |

🟢 Todos os campos confirmados no código.

---

## 2. ResearchResult (TypedDict)

Fonte: `apps/streamlit/agents/state.py`

| Campo     | Tipo  | Obrigatório | Descrição                          |
| --------- | ----- | ----------- | ---------------------------------- |
| `title`   | `str` | sim         | Título do resultado                |
| `source`  | `str` | sim         | Domínio da fonte                   |
| `url`     | `str` | sim         | URL completa                       |
| `snippet` | `str` | sim         | Trecho do conteúdo (max 300 chars) |
| `date`    | `str` | não         | Data de publicação                 |

🟢

---

## 3. SlideContent (TypedDict)

Fonte: `apps/streamlit/agents/state.py`

| Campo          | Tipo        | Obrigatório | Descrição                  |
| -------------- | ----------- | ----------- | -------------------------- |
| `slide_number` | `int`       | sim         | Número sequencial do slide |
| `title`        | `str`       | sim         | Título do slide            |
| `subtitle`     | `str`       | não         | Subtítulo (1 linha)        |
| `content`      | `list[str]` | sim         | Bullets/parágrafos (max 6) |
| `notes`        | `str`       | não         | Notas do apresentador      |

🟢

---

## 4. NodeModelConfig (dataclass)

Fonte: `apps/streamlit/agents/model_selector.py`

| Campo                | Tipo             | Descrição                    |
| -------------------- | ---------------- | ---------------------------- |
| `node_name`          | `str`            | Nome do node no pipeline     |
| `complexity`         | `TaskComplexity` | NONE / SIMPLE / COMPLEX      |
| `model`              | `str`            | Nome do modelo LLM           |
| `max_tokens`         | `int`            | Limite de tokens             |
| `temperature`        | `float`          | Temperatura de geração       |
| `estimated_cost_usd` | `float`          | Custo estimado por invocação |

🟢

---

## 5. TaskComplexity (Enum)

Fonte: `apps/streamlit/agents/model_selector.py`

| Valor     | Significado                 |
| --------- | --------------------------- |
| `NONE`    | Sem LLM (determinístico)    |
| `SIMPLE`  | MiniMax M2.5 ou gpt-4o-mini |
| `COMPLEX` | GPT-4o                      |

🟢

---

## 6. Settings (classe)

Fonte: `apps/streamlit/config.py`

| Campo                      | Tipo   | Env Var                    | Default     |
| -------------------------- | ------ | -------------------------- | ----------- |
| `openai_api_key`           | `str`  | `OPENAI_API_KEY`           | ""          |
| `minimax_api_key`          | `str`  | `MINIMAX_API_KEY`          | ""          |
| `tavily_api_key`           | `str`  | `TAVILY_API_KEY`           | ""          |
| `model_selection_strategy` | `str`  | `MODEL_SELECTION_STRATEGY` | "auto"      |
| `exports_dir`              | `Path` | `EXPORTS_DIR`              | "exports"   |
| `templates_dir`            | `Path` | `TEMPLATES_DIR`            | "templates" |

🟢

---

## 7. Template Registry Entry

Fonte: `templates/registry.json`

| Campo         | Tipo   | Obrigatório | Descrição                                      |
| ------------- | ------ | ----------- | ---------------------------------------------- |
| `id`          | `str`  | sim         | Identificador slug (kebab-case)                |
| `name`        | `str`  | sim         | Nome de exibição                               |
| `description` | `str`  | sim         | Descrição do template                          |
| `colors`      | `dict` | sim         | {primary, secondary, accent, background, text} |
| `fonts`       | `dict` | sim         | {title, body}                                  |

🟢

---

## 8. Template Manifest (manifest.json)

Fonte: `apps/streamlit/template_register.py:register_template`

| Campo         | Tipo        | Obrigatório | Descrição                     |
| ------------- | ----------- | ----------- | ----------------------------- |
| `id`          | `str`       | sim         | Identificador slug            |
| `name`        | `str`       | sim         | Nome de exibição              |
| `description` | `str`       | sim         | Descrição                     |
| `colors`      | `dict`      | sim         | Paleta de 5 cores             |
| `fonts`       | `dict`      | sim         | Fontes título/corpo           |
| `logo`        | `str\|null` | não         | Filename do logo extraído     |
| `footer`      | `str`       | não         | Texto de rodapé               |
| `layouts`     | `list[str]` | não         | Nomes dos layouts disponíveis |

🟢

---

## 9. Proposal Data (dict runtime)

Fonte: `apps/streamlit/app.py` (modo Proposta)

| Campo               | Tipo         | Descrição                           |
| ------------------- | ------------ | ----------------------------------- |
| `nome_projeto`      | `str`        | Nome do projeto                     |
| `cliente`           | `str`        | Cliente/organização                 |
| `responsavel`       | `str`        | Responsável pela proposta           |
| `data_proposta`     | `str`        | Data (ISO format)                   |
| `problema`          | `str`        | Problema identificado               |
| `solucao`           | `str`        | Solução proposta                    |
| `diferenciais`      | `str`        | Diferenciais (opcional)             |
| `escopo_inclui`     | `str`        | O que está no escopo                |
| `escopo_nao_inclui` | `str`        | O que não está no escopo            |
| `tecnologias`       | `str`        | Stack tecnológico                   |
| `etapas`            | `list[dict]` | [{nome, entregas, duracao_semanas}] |
| `valor_total`       | `str`        | Valor total do projeto              |
| `forma_pagamento`   | `str`        | Forma de pagamento                  |
| `prazo_total`       | `str`        | Prazo estimado                      |
| `validade_proposta` | `str`        | Validade da proposta                |
| `equipe`            | `str`        | Papéis e profissionais              |
| `template`          | `str`        | Template visual escolhido           |

🟢
