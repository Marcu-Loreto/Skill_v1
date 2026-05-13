# Dependências — Skill_Presentation

> Gerado pelo Scout em 2026-05-11
> Escala de confiança: 🟢 CONFIRMADO | 🟡 INFERIDO | 🔴 LACUNA

---

## Gerenciador de Pacotes

| Gerenciador | Arquivo de Lock | Versão |
| ----------- | --------------- | ------ |
| uv          | pyproject.toml  | — 🟢   |

---

## Dependências Python (Identificadas via imports) 🟡

> O `pyproject.toml` declara `dependencies = []`. As dependências reais foram inferidas a partir dos imports no código-fonte.

### Core

| Pacote             | Uso                                    | Criticidade |
| ------------------ | -------------------------------------- | ----------- |
| `streamlit`        | Interface web (UI principal)           | Alta        |
| `langchain-openai` | Integração com OpenAI (ChatOpenAI)     | Alta        |
| `langchain-core`   | Messages (SystemMessage, HumanMessage) | Alta        |
| `python-dotenv`    | Carregamento de .env                   | Média       |

### Pesquisa Web

| Pacote                | Uso                                   | Criticidade |
| --------------------- | ------------------------------------- | ----------- |
| `tavily-python`       | Pesquisa web via Tavily API           | Média       |
| `langchain-community` | DuckDuckGoSearchAPIWrapper (fallback) | Baixa       |

### Conversão / Export

| Pacote           | Uso                                        | Criticidade |
| ---------------- | ------------------------------------------ | ----------- |
| `python-pptx`    | Geração e leitura de .pptx                 | Alta        |
| `beautifulsoup4` | Parsing de HTML para validação e conversão | Média       |
| `lxml`           | Parser HTML (backend do BeautifulSoup)     | Média       |

### Stdlib (sem instalação)

| Módulo        | Uso                            |
| ------------- | ------------------------------ |
| `pathlib`     | Manipulação de caminhos        |
| `json`        | Leitura/escrita de JSON        |
| `re`          | Regex para parsing             |
| `datetime`    | Timestamps em nomes de arquivo |
| `subprocess`  | Chamada ao script convert.py   |
| `shutil`      | Cópia de arquivos (templates)  |
| `tempfile`    | Arquivos temporários (upload)  |
| `functools`   | lru_cache para singletons      |
| `dataclasses` | NodeModelConfig                |
| `enum`        | TaskComplexity                 |
| `typing`      | Type hints                     |

---

## APIs Externas

| Serviço              | Variável de Ambiente | Obrigatório                    |
| -------------------- | -------------------- | ------------------------------ |
| OpenAI (GPT-4o-mini) | `OPENAI_API_KEY`     | Sim (para geração com LLM)     |
| MiniMax (M2.5)       | `MINIMAX_API_KEY`    | Não (fallback para OpenAI)     |
| Tavily (web search)  | `TAVILY_API_KEY`     | Não (fallback para DuckDuckGo) |

---

## Estratégia de Modelos

| Node            | Complexidade          | Modelo      | Custo estimado |
| --------------- | --------------------- | ----------- | -------------- |
| Research        | Nenhuma (web search)  | —           | $0.000         |
| Structure       | Simple                | gpt-4o-mini | $0.002         |
| Content         | Complex               | gpt-4o-mini | $0.005         |
| HTML Generation | Nenhuma (template)    | —           | $0.000         |
| PPTX Conversion | Nenhuma (python-pptx) | —           | $0.000         |
| Validation      | Nenhuma (checks)      | —           | $0.000         |

Custo total estimado por apresentação: ~$0.007

---

## Observações

- 🟡 O `pyproject.toml` não lista dependências explícitas (`dependencies = []`). Provavelmente o ambiente é gerenciado manualmente ou via `requirements.txt` não presente na raiz.
- 🟢 O código usa `gpt-4o-mini` para todas as tarefas (tanto simple quanto complex), apesar dos comentários mencionarem GPT-4o e MiniMax M2.5.
- 🟢 O MiniMax é tentado primeiro no `app_chat.py` como modelo preferencial (custo zero), com fallback para `gpt-4o-mini`.
