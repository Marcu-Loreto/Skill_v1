# ADR-002: Uso Exclusivo de gpt-4o-mini (divergência do design)

> Status: 🟢 CONFIRMADO (código) / 🟡 INFERIDO (motivo)
> Data estimada: durante desenvolvimento
> Contexto: Arqueologia de código

---

## Contexto

O `model_selector.py` define um sistema sofisticado de seleção de modelo por complexidade de tarefa:

- `NONE` → sem LLM (research, html, pptx, validation)
- `SIMPLE` → MiniMax M2.5 ou gpt-4o-mini (structure)
- `COMPLEX` → GPT-4o (content)

Porém, `config.py:get_model_for_task()` ignora completamente essa lógica:

```python
def get_model_for_task(self, complexity: str = "simple") -> str:
    # Todas as estratégias retornam "gpt-4o-mini"
    return "gpt-4o-mini"
```

## Decisão

Usar `gpt-4o-mini` para todas as tarefas que requerem LLM, independente da complexidade declarada.

## Consequências

**Positivas:**

- Custo reduzido (~$0.005 por execução vs. ~$0.20 com GPT-4o)
- Latência menor
- Simplicidade — um modelo para tudo

**Negativas:**

- Qualidade de escrita inferior ao GPT-4o para conteúdo complexo
- `model_selector.py` é código morto (nunca efetivamente usado)
- Confusão para desenvolvedores — documentação diverge da realidade

## Alternativas consideradas 🟡

1. **Mix GPT-4o + gpt-4o-mini** — conforme design original do model_selector
2. **MiniMax M2.5 para simple, GPT-4o para complex** — conforme documentação
3. **gpt-4o-mini para tudo** — escolhida (provavelmente por custo durante desenvolvimento)

## Nota

O modo chat (`app_chat.py`) tem sua própria fallback chain separada (MiniMax → gpt-4o-mini) que funciona independente de `config.py`.
