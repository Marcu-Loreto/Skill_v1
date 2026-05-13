# Máquinas de Estado — Skill_Presentation

> Gerado pelo Detetive em 2026-05-11
> Escala de confiança: 🟢 CONFIRMADO | 🟡 INFERIDO | 🔴 LACUNA

---

## 1. Pipeline de Geração (PresentationState) 🟢

O pipeline é uma máquina de estados linear com retry condicional na validação.

### Estados do Pipeline

| Estado           | Node responsável             | Campos produzidos                                       |
| ---------------- | ---------------------------- | ------------------------------------------------------- |
| `INIT`           | app.py (construção do state) | tema, publico, tom, num_slides, template, formato_saida |
| `RESEARCHED`     | research_node                | research_queries, research_results, selected_data       |
| `STRUCTURED`     | structure_node               | slide_titles                                            |
| `CONTENT_READY`  | content_node                 | slides                                                  |
| `HTML_GENERATED` | html_node                    | html_content, html_path                                 |
| `PPTX_GENERATED` | pptx_node                    | pptx_path                                               |
| `VALIDATED`      | validation_node              | is_valid, error, validation_metrics                     |

### Diagrama de Transições

```mermaid
stateDiagram-v2
    [*] --> INIT : Usuário clica "Gerar"
    INIT --> RESEARCHED : research_node()
    RESEARCHED --> STRUCTURED : structure_node()
    STRUCTURED --> CONTENT_READY : content_node() + quality_standards
    CONTENT_READY --> HTML_GENERATED : html_node()
    HTML_GENERATED --> PPTX_GENERATED : pptx_node() [se PPTX solicitado]
    HTML_GENERATED --> VALIDATED : validation_node() [se só HTML]
    PPTX_GENERATED --> VALIDATED : validation_node()
    VALIDATED --> CONTENT_READY : retry [se !is_valid && retry_count < 2]
    VALIDATED --> [*] : sucesso [is_valid == true]
    VALIDATED --> [*] : falha final [retry_count >= 2]
```

### Condições de Transição

| De → Para                       | Condição                                      | Confiança |
| ------------------------------- | --------------------------------------------- | --------- | ------------------- | --- |
| INIT → RESEARCHED               | Sempre (tema pode ser vazio → error no state) | 🟢        |
| RESEARCHED → STRUCTURED         | Sempre                                        | 🟢        |
| STRUCTURED → CONTENT_READY      | Sempre (fallback determinístico se LLM falha) | 🟢        |
| CONTENT_READY → HTML_GENERATED  | `slides` não vazio                            | 🟢        |
| HTML_GENERATED → PPTX_GENERATED | `"PPTX (editável)" in formato_saida`          | 🟢        |
| PPTX_GENERATED → VALIDATED      | Sempre                                        | 🟢        |
| VALIDATED → retry               | `!is_valid && _retry_count < 2`               | 🟢        |
| VALIDATED → fim                 | `is_valid                                     |           | \_retry_count >= 2` | 🟢  |

---

## 2. Fallback Chain de LLMs (Modo Chat) 🟢

```mermaid
stateDiagram-v2
    [*] --> CHECK_MINIMAX : Início
    CHECK_MINIMAX --> TRY_MINIMAX : has_minimax == true
    CHECK_MINIMAX --> USE_GPT4O_MINI : has_minimax == false
    TRY_MINIMAX --> MINIMAX_OK : ping sucesso
    TRY_MINIMAX --> USE_GPT4O_MINI : ping falha
    MINIMAX_OK --> GENERATE : invoke MiniMax
    USE_GPT4O_MINI --> GENERATE : invoke gpt-4o-mini
    GENERATE --> [*] : resposta HTML
```

---

## 3. Validação com Retry 🟢

```mermaid
stateDiagram-v2
    [*] --> VALIDATE
    VALIDATE --> PASS : errors == []
    VALIDATE --> FAIL : errors > 0
    FAIL --> RETRY : retry_count < 2
    FAIL --> FINAL_FAIL : retry_count >= 2
    RETRY --> VALIDATE : re-executa pipeline parcial
    PASS --> [*]
    FINAL_FAIL --> [*]
```

**Nota**: O retry incrementa `_retry_count` e seta `_should_retry = True`, mas a lógica de re-execução do pipeline parcial não está implementada no `app.py` — o validation_node apenas sinaliza. 🟡

---

## 4. Template Registration 🟢

```mermaid
stateDiagram-v2
    [*] --> UPLOAD : Usuário faz upload
    UPLOAD --> CHECK_FORMAT
    CHECK_FORMAT --> PROCESS_PPTX : .pptx
    CHECK_FORMAT --> CONVERT_PDF : .pdf
    CONVERT_PDF --> PROCESS_PPTX : conversão OK
    CONVERT_PDF --> ERROR : conversão falha
    PROCESS_PPTX --> EXTRACT_COLORS
    EXTRACT_COLORS --> EXTRACT_FONTS
    EXTRACT_FONTS --> EXTRACT_LOGO
    EXTRACT_LOGO --> SAVE_MANIFEST
    SAVE_MANIFEST --> UPDATE_REGISTRY
    UPDATE_REGISTRY --> [*] : template disponível
    ERROR --> [*] : mensagem de erro
```

---

## 5. Seleção de Modelo por Node 🟡

```mermaid
stateDiagram-v2
    [*] --> CHECK_NODE_TYPE
    CHECK_NODE_TYPE --> NO_LLM : research, html, pptx, validation
    CHECK_NODE_TYPE --> NEED_LLM : structure, content
    NEED_LLM --> CHECK_API_KEY
    CHECK_API_KEY --> USE_LLM : has_openai == true
    CHECK_API_KEY --> DETERMINISTIC : has_openai == false
    USE_LLM --> INVOKE_MODEL : get_model_for_task()
    INVOKE_MODEL --> SUCCESS : resposta OK
    INVOKE_MODEL --> DETERMINISTIC : exceção
    NO_LLM --> DETERMINISTIC
    DETERMINISTIC --> [*]
    SUCCESS --> [*]
```

**Nota**: Apesar do `model_selector.py` definir complexidades diferentes por node, `config.py` sempre retorna `gpt-4o-mini`. A máquina de estados real é mais simples que a intencionada.
