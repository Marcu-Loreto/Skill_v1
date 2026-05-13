# ADR-003: Fallback Determinístico Universal em Todos os Nodes

> Status: 🟢 CONFIRMADO
> Data estimada: design inicial
> Contexto: Arqueologia de código

---

## Contexto

Cada node que usa LLM implementa um path alternativo determinístico que é ativado quando:

- API key não está configurada (`has_openai == False`)
- Chamada ao LLM lança exceção (timeout, rate limit, erro de rede)

Exemplos:

- `structure_node` → `generate_structure_deterministic()` usa framework template fixo
- `content_node` → `generate_content_deterministic()` distribui snippets de pesquisa nos slides
- `research_node` → fallback DuckDuckGo se Tavily falhar

## Decisão

Todo node com dependência de LLM DEVE ter um fallback determinístico que produz output válido (mesmo que de menor qualidade).

## Consequências

**Positivas:**

- Sistema nunca falha completamente — sempre produz algum resultado
- Funciona sem API keys (modo demo/offline)
- Resiliência a falhas de rede ou rate limiting

**Negativas:**

- Qualidade degradada significativamente no fallback (slides genéricos, sem dados reais)
- Usuário pode não perceber que está recebendo output de fallback
- Código duplicado (lógica LLM + lógica determinística em cada node)

## Alternativas consideradas 🟡

1. **Falhar com erro claro** — informar usuário que API key é necessária
2. **Queue com retry** — esperar e tentar novamente
3. **Fallback silencioso** — escolhida (prioriza "sempre funcionar")
