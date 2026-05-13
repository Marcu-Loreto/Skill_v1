# Domínio — Skill_Presentation

> Gerado pelo Detetive em 2026-05-11
> Escala de confiança: 🟢 CONFIRMADO | 🟡 INFERIDO | 🔴 LACUNA

---

## Glossário de Domínio

| Termo                     | Definição                                                                                                                      | Confiança |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------ | --------- |
| Apresentação              | Artefato final gerado pelo sistema — conjunto de slides em HTML e/ou PPTX                                                      | 🟢        |
| Slide                     | Unidade atômica de conteúdo visual: título + subtítulo + bullets + notas do apresentador                                       | 🟢        |
| Pipeline                  | Cadeia sequencial de 6 nodes que transforma um tema em apresentação: Research → Structure → Content → HTML → PPTX → Validation | 🟢        |
| Node                      | Função pura `state → state` que executa uma etapa do pipeline                                                                  | 🟢        |
| State (PresentationState) | Dicionário tipado que carrega todos os dados entre nodes — single source of truth                                              | 🟢        |
| Template                  | Identidade visual corporativa extraída de um .pptx: cores, fontes, logo                                                        | 🟢        |
| Registry                  | Arquivo `templates/registry.json` que indexa todos os templates registrados                                                    | 🟢        |
| Manifest                  | Metadados completos de um template (cores, fontes, logo, layouts) salvos em `templates/<id>/manifest.json`                     | 🟢        |
| Quality Score             | Pontuação 0–100 calculada deterministicamente: 100 − (títulos genéricos × 5) − (dados sem citação × 3)                         | 🟢        |
| Trusted Domain            | Domínio de fonte confiável (mckinsey, gartner, gov.br, etc.) que recebe boost +0.3 no ranking                                  | 🟢        |
| Blocked Domain            | Domínio proibido (pinterest, facebook, etc.) filtrado dos resultados de pesquisa                                               | 🟢        |
| Fallback                  | Estratégia de degradação graceful: se LLM falha, node usa lógica determinística                                                | 🟢        |
| Fallback Chain            | Cadeia de LLMs no modo chat: MiniMax M2.5 → gpt-4o-mini                                                                        | 🟢        |
| Framework de Slides       | Template estrutural fixo (11 títulos) que define a ordem lógica dos slides                                                     | 🟢        |
| Modo Free                 | Apresentação livre — usuário fornece tema e o sistema pesquisa + gera                                                          | 🟢        |
| Modo Proposal             | Proposta de projeto — formulário estruturado com campos fixos                                                                  | 🟢        |
| Modo Chat                 | Interface simplificada — prompt livre gera HTML diretamente via LLM                                                            | 🟢        |

---

## Regras de Negócio

### RN-01: Limites de Conteúdo por Slide 🟢

| Regra                         | Valor                      | Enforcement                                                 |
| ----------------------------- | -------------------------- | ----------------------------------------------------------- |
| Máximo de bullets por slide   | 6                          | `quality_standards.py` trunca para 5 + indicador "+N itens" |
| Máximo de palavras por bullet | 18                         | `quality_standards.py` trunca com "..."                     |
| Formato obrigatório           | 16:9 (13.333 × 7.5 inches) | Constante em quality_standards + pptx_node                  |
| Idioma obrigatório            | pt-BR                      | Definido em prompts e quality_standards                     |

### RN-02: Qualidade de Títulos 🟢

Títulos genéricos são proibidos. Regex de detecção:

- `^slide \d+$`, `^introdução$`, `^conclusão$`, `^desenvolvimento$`
- `^conteúdo$`, `^informações$`, `^dados$`, `^overview$`, `^introduction$`

Penalidade: −5 pontos no quality score por título genérico detectado.

### RN-03: Citação Obrigatória de Dados 🟢

Qualquer bullet que contenha dados quantitativos (%, R$, $, milhões, bilhões, mil) DEVE ter citação com fonte e ano. Padrões aceitos:

- `(Fonte, 2024)` ou `(Fonte, 20XX)`
- `Fonte: ...`
- `[Fonte]`

Penalidade: −3 pontos no quality score por slide com dado sem citação.

### RN-04: Pesquisa Web — Filtragem de Fontes 🟢

| Categoria            | Comportamento                            |
| -------------------- | ---------------------------------------- |
| Trusted Domains (17) | Boost +0.3 no score de ranking           |
| Blocked Domains (7)  | Excluídos completamente dos resultados   |
| Domínios duplicados  | Penalidade −0.2 no score                 |
| Snippets vazios      | Penalidade −0.3                          |
| Snippets < 50 chars  | Penalidade −0.1                          |
| Resultado final      | Top 8 por score, top 5 usados nos slides |

### RN-05: Retry de Validação 🟢

- Máximo de retries: 2
- Condição de retry: `is_valid == False` e `retry_count < 2`
- Campo interno: `_retry_count` e `_should_retry` no state

### RN-06: Validação de Arquivos Gerados 🟢

| Verificação        | HTML              | PPTX              |
| ------------------ | ----------------- | ----------------- |
| Arquivo existe     | ✓                 | ✓                 |
| Tamanho mínimo     | 500 bytes         | 5.000 bytes       |
| Tamanho máximo     | 5 MB              | —                 |
| Slides encontrados | ≥ 50% do esperado | ≥ 50% do esperado |
| Slides vazios      | ≤ 30% do total    | —                 |
| Slides com texto   | —                 | ≥ 50% do total    |
| Navegação presente | ✓ (botões)        | —                 |

### RN-07: Seleção de Modelo (Intenção vs. Implementação) 🟡

| Intenção documentada   | Implementação real                   |
| ---------------------- | ------------------------------------ |
| Simple → MiniMax M2.5  | Todas as estratégias → `gpt-4o-mini` |
| Complex → GPT-4o       | Todas as estratégias → `gpt-4o-mini` |
| Auto → mix inteligente | Todas as estratégias → `gpt-4o-mini` |

**Divergência confirmada**: `config.py:get_model_for_task()` retorna `"gpt-4o-mini"` para qualquer valor de `complexity` ou `strategy`. Os comentários e o `model_selector.py` descrevem um sistema de seleção que não está implementado.

### RN-08: Fallback Chain no Modo Chat 🟢

```
1. Se has_minimax → tenta MiniMax M2.5 (base_url: api.minimaxi.chat/v1, max_tokens: 32000)
2. Ping test → se falhar, llm = None
3. Se llm == None → usa gpt-4o-mini (max_tokens: 16000)
```

### RN-09: Limites de Input do Usuário 🟢

| Campo                       | Min | Max | Default             |
| --------------------------- | --- | --- | ------------------- |
| Número de slides            | 5   | 25  | 12                  |
| Número de etapas (proposta) | 2   | 10  | 4                   |
| Upload de template          | —   | —   | .pptx e .pdf apenas |

### RN-10: Adaptação de Framework ao Número de Slides 🟢

- Se `num_slides > len(framework)`: insere slides "Desenvolvimento — Parte N" no meio
- Se `num_slides < len(framework)`: remove do meio, mantém 2 primeiros e 2 últimos
- Slides opcionais (Agenda, Referências) removidos conforme flags do usuário

### RN-11: Detecção de Logo em Templates 🟢

1. Busca imagens no slide master (`shape_type == 13`)
2. Fallback: imagens pequenas (< 3 inches) no primeiro slide
3. Salva como `logo.{ext}` no diretório do template

### RN-12: Cores Default de Template 🟢

Se extração de cores falhar: `primary=#0066CC`, `secondary=#003366`, `accent=#00AAFF`

### RN-13: Validação de API Keys 🟢

| Key     | Condição de "válida"                   |
| ------- | -------------------------------------- |
| OpenAI  | Não vazia E não começa com "sk-your"   |
| MiniMax | Não vazia E ≠ "your-minimax-key-here"  |
| Tavily  | Não vazia E não começa com "tvly-your" |

### RN-14: Geração de Queries de Pesquisa 🟢

Heurística sem LLM:

1. Query original: `{tema}`
2. Query com dados: `{tema} dados estatísticas 2025 2026`
3. Query em inglês: palavras > 3 chars do tema + "statistics report 2025"

### RN-15: Dark Theme Forçado no Modo Chat 🟢

O system prompt do modo chat força dark theme independente do template selecionado. Mínimo 5 slides.

---

## Regras Implícitas (não documentadas no código) 🟡

| Regra                                             | Evidência                                   | Confiança |
| ------------------------------------------------- | ------------------------------------------- | --------- |
| Proposta de Projeto é Fase 2 — não implementada   | TODOs em app.py, placeholders nos botões    | 🟢        |
| `html_generator.md` prompt existe mas não é usado | html_node é 100% determinístico             | 🟢        |
| Sem autenticação — qualquer pessoa acessa         | Nenhum middleware de auth, sem login        | 🟡        |
| Sem persistência de sessão entre reloads          | Apenas `st.session_state` (memória)         | 🟢        |
| Sem rate limiting nas chamadas LLM                | Nenhum throttle ou queue implementado       | 🟡        |
| Sem tratamento de timeout em chamadas LLM         | Nenhum `timeout` configurado nos ChatOpenAI | 🟡        |
| Cache de prompts com LRU maxsize=10               | `prompt_loader.py:@lru_cache(maxsize=10)`   | 🟢        |
| Exports nunca são limpos automaticamente          | Pasta `exports/` cresce indefinidamente     | 🟡        |

---

## Invariantes do Sistema 🟢

1. **Imutabilidade do state entre nodes**: cada node recebe `state` e retorna `{**state, ...novos_campos}` — nunca muta in-place
2. **Fallback universal**: todo node com LLM tem path determinístico se API falhar
3. **Prompts externalizados**: nenhum system prompt hardcoded nos nodes (exceto `QUALITY_PROMPT_SUFFIX`)
4. **Singleton de config**: `get_settings()` com `@lru_cache()` garante instância única
5. **Formato 16:9 invariável**: todas as saídas (HTML e PPTX) usam 13.333 × 7.5 inches
