# Análise de Código — Skill_Presentation

> Gerado pelo Arqueólogo em 2026-05-11
> Escala de confiança: 🟢 CONFIRMADO | 🟡 INFERIDO | 🔴 LACUNA

---

## Módulo 1: Pipeline (agents/)

### Propósito

Pipeline de geração de apresentações com 6 nodes sequenciais. Cada node recebe um `state: dict` e retorna o state atualizado.

### Fluxo Principal

```
Research → Structure → Content → HTML → PPTX → Validation
```

### Funções Principais

| Função            | Arquivo                     | Parâmetros    | Retorno                                  | Confiança |
| ----------------- | --------------------------- | ------------- | ---------------------------------------- | --------- |
| `research_node`   | `agents/research_node.py`   | `state: dict` | `dict` (state + research_results)        | 🟢        |
| `structure_node`  | `agents/structure_node.py`  | `state: dict` | `dict` (state + slide_titles)            | 🟢        |
| `content_node`    | `agents/content_node.py`    | `state: dict` | `dict` (state + slides)                  | 🟢        |
| `html_node`       | `agents/html_node.py`       | `state: dict` | `dict` (state + html_content, html_path) | 🟢        |
| `pptx_node`       | `agents/pptx_node.py`       | `state: dict` | `dict` (state + pptx_path)               | 🟢        |
| `validation_node` | `agents/validation_node.py` | `state: dict` | `dict` (state + is_valid, error)         | 🟢        |

### Algoritmos Não-Triviais

#### 1. Geração de Queries de Pesquisa (research_node.py)

- Heurística sem LLM: tema original + tema com "dados estatísticas 2025 2026" + keywords em inglês
- Extração de palavras > 3 caracteres para query em inglês 🟢

#### 2. Ranking de Resultados (research_node.py:filter_and_rank_results)

- Score base do Tavily + boost +0.3 para domínios confiáveis
- Penalidade -0.2 para domínios duplicados
- Penalidade -0.3 para snippets vazios, -0.1 para snippets < 50 chars
- Ordenação decrescente, top 8 🟢

#### 3. Adaptação de Framework de Slides (structure_node.py:generate_structure_deterministic)

- Se slides > framework: remove do meio, mantém 2 primeiros e 2 últimos
- Se slides < framework: insere "Desenvolvimento — Parte N" no meio
- Remove slides opcionais (Agenda, Referências) conforme flags 🟢

#### 4. Parsing de Resposta LLM (content_node.py:parse_content_response)

- Split por marcador `---SLIDE---`
- Extração de TÍTULO, SUBTÍTULO, CONTEÚDO, NOTAS via regex
- Padding com slides genéricos se LLM retornar menos que o esperado 🟢

#### 5. Quality Standards (quality_standards.py:apply_quality_standards)

- Trunca bullets > 6 por slide (mantém 5 + indicador "+N itens")
- Trunca bullets > 18 palavras com "..."
- Score: 100 - (títulos genéricos × 5) - (dados sem citação × 3) 🟢

#### 6. Detecção de Tema Dark/Light (html_node.py)

- Compara `background` com lista hardcoded de cores escuras
- Ajusta cores de subtítulo, nav, border conforme resultado 🟢

### Regras de Negócio

| Regra                                                     | Localização                            | Confiança |
| --------------------------------------------------------- | -------------------------------------- | --------- |
| Máximo 6 bullets por slide                                | `quality_standards.py:12`              | 🟢        |
| Máximo 18 palavras por bullet                             | `quality_standards.py:13`              | 🟢        |
| Formato 16:9 (13.333 × 7.5 inches)                        | `quality_standards.py:14-15`           | 🟢        |
| Idioma obrigatório: pt-BR                                 | `quality_standards.py:17`              | 🟢        |
| Títulos genéricos proibidos (regex)                       | `quality_standards.py:20-29`           | 🟢        |
| Dados devem ter citação com fonte                         | `quality_standards.py:check_citations` | 🟢        |
| Retry máximo de validação: 2                              | `validation_node.py:validation_node`   | 🟢        |
| Domínios bloqueados (pinterest, facebook, etc.)           | `research_node.py:BLOCKED_DOMAINS`     | 🟢        |
| Domínios confiáveis priorizados (mckinsey, gartner, etc.) | `research_node.py:TRUSTED_DOMAINS`     | 🟢        |

### Constantes e Configurações

| Constante               | Valor              | Arquivo              |
| ----------------------- | ------------------ | -------------------- |
| `MAX_BULLETS_PER_SLIDE` | 6                  | quality_standards.py |
| `MAX_WORDS_PER_BULLET`  | 18                 | quality_standards.py |
| `SLIDE_WIDTH_INCHES`    | 13.333             | quality_standards.py |
| `SLIDE_HEIGHT_INCHES`   | 7.5                | quality_standards.py |
| `TRUSTED_DOMAINS`       | 17 domínios        | research_node.py     |
| `BLOCKED_DOMAINS`       | 7 domínios         | research_node.py     |
| `FRAMEWORK_FREE`        | 11 slides template | structure_node.py    |
| `FRAMEWORK_PROPOSAL`    | 11 slides template | structure_node.py    |

---

## Módulo 2: UI Forms (app.py)

### Propósito

Interface Streamlit com 3 modos: Apresentação Livre, Proposta de Projeto, Gerenciar Templates.

### Fluxo de Controle

1. Sidebar: seleção de modo via `st.radio`
2. Modo "Apresentação Livre":
   - Formulário: tema, público, tom, num_slides, template, formato
   - Opções avançadas: referências, agenda, idioma pesquisa
   - Botão "Gerar" → executa pipeline sequencial com progress bar
   - Preview: tabs (HTML inline, lista de slides, downloads)
3. Modo "Proposta de Projeto":
   - Formulário estruturado: identificação, problema/solução, escopo, tecnologia, etapas, investimento, equipe
   - Botão "Gerar Proposta" → placeholder (TODO: integração Fase 2)
4. Modo "Gerenciar Templates":
   - Upload .pptx/.pdf → extração de cores/fontes/logo
   - Lista de templates registrados com preview

### Regras de Negócio

| Regra                                     | Localização                                                   | Confiança |
| ----------------------------------------- | ------------------------------------------------------------- | --------- |
| Botão desabilitado se tema vazio          | `app.py:disabled=not tema`                                    | 🟢        |
| Proposta requer nome + problema + solução | `app.py:disabled=not (nome_projeto and problema and solucao)` | 🟢        |
| Slides: min 5, max 25, default 12         | `app.py:st.slider`                                            | 🟢        |
| Etapas: min 2, max 10, default 4          | `app.py:st.number_input`                                      | 🟢        |
| Upload aceita apenas .pptx e .pdf         | `app.py:st.file_uploader(type=["pptx", "pdf"])`               | 🟢        |
| Proposta modo "Fase 2" — não implementado | `app.py:TODO comments`                                        | 🟢        |

---

## Módulo 3: UI Chat (app_chat.py)

### Propósito

Interface chat simplificada. Usuário digita prompt livre, sistema gera HTML diretamente via LLM.

### Fluxo de Controle

1. Chat input → pesquisa web (research_node) → contexto de dados
2. LLM chain: MiniMax M2.5 (tentativa) → fallback gpt-4o-mini
3. Resposta: HTML completo → salva em `exports/` → download button

### Algoritmos

#### Fallback Chain de LLMs

```python
if settings.has_minimax:
    try MiniMax-M2.5 (base_url: api.minimaxi.chat/v1, max_tokens: 32000)
    ping test → se falhar, llm = None
if not llm:
    use gpt-4o-mini (max_tokens: 16000)
```

🟢

#### Limpeza de Resposta

- Remove `html e ` do início/fim da resposta LLM 🟢

### Regras de Negócio

| Regra                                    | Localização                  | Confiança |
| ---------------------------------------- | ---------------------------- | --------- |
| MiniMax tentado primeiro (custo zero)    | `app_chat.py:fallback chain` | 🟢        |
| Mínimo 5 slides no system prompt         | `app_chat.py:system_msg`     | 🟢        |
| Dark theme forçado no chat mode          | `app_chat.py:system_msg`     | 🟢        |
| Slug do filename: max 40 chars do prompt | `app_chat.py:slug`           | 🟢        |

---

## Módulo 4: Templates (template_register.py + templates/)

### Propósito

Sistema de templates corporativos. Upload de .pptx → extração automática de cores, fontes, logo → registro no `registry.json`.

### Funções Principais

| Função                          | Parâmetros                        | Retorno            | Confiança |
| ------------------------------- | --------------------------------- | ------------------ | --------- |
| `extract_theme_colors(prs)`     | Presentation                      | dict (5 cores)     | 🟢        |
| `extract_fonts(prs)`            | Presentation                      | dict (title, body) | 🟢        |
| `extract_logo(prs, output_dir)` | Presentation, Path                | Optional[str]      | 🟢        |
| `get_slide_layouts(prs)`        | Presentation                      | list[str]          | 🟢        |
| `register_template(...)`        | pptx_path, name, id, desc, footer | dict (manifest)    | 🟢        |
| `list_templates()`              | —                                 | list[dict]         | 🟢        |
| `delete_template(id)`           | template_id                       | bool               | 🟢        |

### Algoritmos

#### Extração de Cores (Heurísticas)

1. Tenta background do slide master → `background`
2. Tenta cores de texto do master → `text`
3. Tenta cores do primeiro slide (exclui preto/branco/cinza) → `primary`, `accent`
4. Defaults: primary=#0066CC, secondary=#003366, accent=#00AAFF 🟢

#### Extração de Logo

1. Busca imagens no slide master (shape_type == 13)
2. Fallback: imagens pequenas (< 3 inches) no primeiro slide
3. Salva como `logo.{ext}` no diretório do template 🟢

### Estrutura de Dados

```
templates/
├── registry.json          # Array de {id, name, description, colors, fonts}
└── <template-id>/
    ├── base.pptx          # Cópia do arquivo original
    ├── manifest.json      # Metadados completos (colors, fonts, logo, layouts)
    └── logo.{ext}         # Logo extraído (se encontrado)
```

🟢

---

## Módulo 5: Prompts (prompt/\*.md)

### Propósito

System prompts dos agentes em arquivos Markdown separados. Carregados em runtime via `prompt_loader.py`.

### Arquivos

| Prompt               | Usado por               | Propósito                      |
| -------------------- | ----------------------- | ------------------------------ |
| `content_agent.md`   | content_node.py         | Redação profissional de slides |
| `structure_agent.md` | structure_node.py       | Estruturação de títulos        |
| `html_generator.md`  | (não usado diretamente) | Referência para geração HTML   |
| `proposal_agent.md`  | (TODO Fase 2)           | Redação de propostas           |

### Padrões nos Prompts

- Todos definem idioma: pt-BR
- Todos limitam: 6 bullets, 18 palavras
- Todos exigem: citação de fontes
- Formato de saída: `---SLIDE---` / `---FIM---` 🟢

---

## Módulo 6: Config (config.py + .env)

### Propósito

Configuração centralizada via dotenv + classe Settings com lru_cache singleton.

### Estrutura

```python
class Settings:
    openai_api_key: str       # OPENAI_API_KEY
    minimax_api_key: str      # MINIMAX_API_KEY
    tavily_api_key: str       # TAVILY_API_KEY
    model_selection_strategy: str  # MODEL_SELECTION_STRATEGY (auto|simple|complex)
    exports_dir: Path         # EXPORTS_DIR (default: "exports")
    templates_dir: Path       # TEMPLATES_DIR (default: "templates")
```

🟢

### Propriedades de Validação

| Property      | Lógica                                     | Confiança |
| ------------- | ------------------------------------------ | --------- |
| `has_openai`  | key não vazia e não começa com "sk-your"   | 🟢        |
| `has_minimax` | key não vazia e ≠ "your-minimax-key-here"  | 🟢        |
| `has_tavily`  | key não vazia e não começa com "tvly-your" | 🟢        |

### Regra de Seleção de Modelo

```python
def get_model_for_task(complexity):
    # Todas as estratégias retornam "gpt-4o-mini"
    # (comentários mencionam MiniMax/GPT-4o mas implementação usa gpt-4o-mini para tudo)
    return "gpt-4o-mini"
```

🟡 Nota: A implementação diverge dos comentários. O código sempre retorna `gpt-4o-mini` independente da estratégia.

---

## Observações Gerais

### Padrões Arquiteturais

- **Pipeline funcional**: cada node é uma função pura `state → state` 🟢
- **Fallback graceful**: LLM → determinístico em todos os nodes 🟢
- **Singleton config**: `@lru_cache()` no `get_settings()` 🟢
- **Prompts externalizados**: nunca hardcoded, sempre em `prompt/*.md` 🟢

### Lacunas Identificadas

- 🔴 Modo "Proposta de Projeto" não implementado (apenas UI, sem backend)
- 🔴 `html_generator.md` prompt não é usado por nenhum node (html_node é determinístico)
- 🟡 `model_selector.py` define custos e complexidades mas `config.py` ignora e usa gpt-4o-mini para tudo
- 🟡 Sem tratamento de rate limiting ou timeout nas chamadas LLM
- 🟡 Sem persistência de sessão (Streamlit session_state apenas em memória)
