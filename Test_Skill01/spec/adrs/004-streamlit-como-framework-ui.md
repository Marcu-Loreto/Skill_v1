# ADR-004: Streamlit como Framework de UI (sem backend separado)

> Status: 🟢 CONFIRMADO
> Data estimada: início do projeto
> Contexto: Arqueologia de código

---

## Contexto

O projeto usa Streamlit como framework full-stack — UI e lógica de negócio no mesmo processo Python. Não há API REST, não há separação frontend/backend, não há banco de dados.

## Decisão

Usar Streamlit como framework monolítico para prototipação rápida, com toda a lógica (UI, pipeline, config) no mesmo processo.

## Consequências

**Positivas:**

- Deploy simples (um processo Python)
- Prototipação extremamente rápida
- Sem necessidade de API, CORS, autenticação
- Hot reload nativo

**Negativas:**

- Sem persistência entre sessões (session_state é volátil)
- Sem multi-user real (cada tab é uma sessão isolada)
- Sem API consumível por outros sistemas
- Escalabilidade limitada (um worker por sessão)
- Re-execução do script inteiro a cada interação

## Alternativas consideradas 🟡

1. **FastAPI + React** — separação completa (mais escalável, mais complexo)
2. **Gradio** — similar ao Streamlit, mais focado em ML
3. **Streamlit** — escolhido (velocidade de prototipação)

## Nota

A estrutura de pastas sugere que uma migração para FastAPI + React está planejada (existem referências em steering files), mas o código atual é 100% Streamlit.
