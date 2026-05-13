# ADR-005: Prompts Externalizados em Arquivos Markdown

> Status: 🟢 CONFIRMADO
> Data estimada: design inicial
> Contexto: Arqueologia de código

---

## Contexto

Todos os system prompts dos agentes LLM são armazenados em arquivos `.md` separados na pasta `prompt/`, carregados em runtime via `prompt_loader.py` com cache LRU (maxsize=10).

Arquivos existentes:

- `prompt/content_agent.md` — redação de slides
- `prompt/structure_agent.md` — estruturação de títulos
- `prompt/html_generator.md` — referência (não usado ativamente)
- `prompt/proposal_agent.md` — propostas (TODO Fase 2)

## Decisão

Nunca hardcodar system prompts no código Python. Sempre usar arquivos Markdown externos carregados via `load_prompt(nome)`.

## Consequências

**Positivas:**

- Prompts editáveis sem alterar código
- Versionamento independente (diff legível em PRs)
- Reutilização entre nodes
- Facilita iteração rápida de prompt engineering

**Negativas:**

- Dependência de filesystem em runtime (pode falhar em ambientes restritos)
- Cache LRU com maxsize=10 pode ser insuficiente se número de prompts crescer
- `html_generator.md` existe mas não é usado — potencial confusão

## Alternativas consideradas 🟡

1. **Prompts inline no código** — mais simples, mas difícil de iterar
2. **Banco de dados de prompts** — versionamento dinâmico, mais complexo
3. **Arquivos Markdown com cache** — escolhida (equilíbrio simplicidade/flexibilidade)

## Exceção

`quality_standards.py` define `QUALITY_PROMPT_SUFFIX` inline — é o único prompt hardcoded no sistema. Provável motivo: é um sufixo técnico (regras de formatação), não um prompt criativo.
