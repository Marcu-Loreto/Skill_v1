# ADR-001: Pipeline Funcional Sequencial (sem grafo LangGraph real)

> Status: 🟡 INFERIDO
> Data estimada: início do projeto
> Contexto: Arqueologia de código (sem Git disponível)

---

## Contexto

O projeto importa LangGraph e LangChain, mas o pipeline é executado como chamadas sequenciais diretas em `app.py`:

```python
pipeline_state = research_node(pipeline_state)
pipeline_state = structure_node(pipeline_state)
pipeline_state = content_node(pipeline_state)
...
```

Não existe um `StateGraph` compilado, nem edges condicionais, nem checkpointing do LangGraph.

## Decisão

Implementar o pipeline como funções puras `state → state` chamadas sequencialmente, sem usar o runtime do LangGraph (grafo compilado, checkpoints, branching).

## Consequências

**Positivas:**

- Simplicidade de debugging — fluxo linear previsível
- Sem overhead do runtime LangGraph
- Fácil de entender para desenvolvedores não familiarizados com LangGraph

**Negativas:**

- Retry parcial não é possível (precisa re-executar do início)
- Sem paralelismo entre nodes independentes
- Sem checkpointing — se Streamlit recarrega, perde tudo
- Divergência entre a arquitetura documentada (LangGraph) e a implementação real

## Alternativas consideradas 🟡

1. **LangGraph StateGraph completo** — com edges condicionais e retry automático
2. **Pipeline com Celery/Redis** — para execução assíncrona com persistência
3. **Abordagem atual** — chamadas sequenciais diretas (escolhida)

Provável motivo da escolha: velocidade de prototipação e simplicidade para MVP.
