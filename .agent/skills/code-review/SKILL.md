---
name: code-review
description: Realiza code review automatizado com foco em boas práticas de engenharia de software, segurança, performance e manutenibilidade. Analisa nós, variáveis, chamadas, dependências e retorna vulnerabilidades classificadas por grau de criticidade. Use esta skill sempre que o usuário pedir revisão de código, code review, análise de segurança de código, auditoria de código, verificação de qualidade, ou mencionar termos como "revise este código", "tem algo errado aqui", "analise vulnerabilidades", "code review", "melhore este código", "está seguro?", "boas práticas".
---

# Code Review — Análise de Qualidade e Segurança

## Objetivo

Realizar revisão de código automatizada, identificando problemas de segurança, performance, manutenibilidade e boas práticas. Entregar um relatório estruturado com vulnerabilidades classificadas por criticidade e sugestões de correção com melhor relação custo-benefício.

## Princípios

- Foco em impacto real, não em pedantismo estilístico
- Priorizar o que pode causar bug em produção, vazamento de dados ou degradação de performance
- Sugestões devem ser acionáveis (mostrar o fix, não apenas apontar o problema)
- Não reportar falsos positivos — se não tem certeza, diga
- Considerar o contexto do projeto (stack, convenções, ambiente)

## Processo de Análise

Ao receber código para revisão, execute estas camadas na ordem:

### Camada 1: Segurança (Crítica)

Buscar:

- Injeção (SQL, command, prompt injection)
- Exposição de dados sensíveis (secrets hardcoded, logs com PII)
- Autenticação/autorização falha (bypass, token sem validação)
- Deserialização insegura
- Path traversal
- SSRF / CSRF
- Dependências com CVEs conhecidas
- Falta de sanitização de input do usuário
- Uso de eval(), exec(), pickle com dados externos

### Camada 2: Confiabilidade (Alta)

Buscar:

- Race conditions
- Falta de tratamento de erros (try/except genérico, erros silenciados)
- Null/None não tratados
- Recursos não liberados (conexões, file handles, locks)
- Loops infinitos potenciais
- Overflow de memória (listas crescendo sem limite)
- Timeouts ausentes em chamadas externas
- Falta de retry/fallback em operações críticas

### Camada 3: Performance (Média)

Buscar:

- Queries N+1
- Operações O(n²) onde O(n) é possível
- Chamadas síncronas que deveriam ser async
- Cache ausente em operações repetitivas e caras
- Serialização/deserialização desnecessária
- Imports pesados no hot path
- Alocações desnecessárias em loops

### Camada 4: Manutenibilidade (Baixa)

Buscar:

- Funções com mais de 50 linhas (complexidade ciclomática alta)
- Código duplicado (DRY violation)
- Nomes de variáveis sem semântica (x, tmp, data, result)
- Acoplamento forte entre módulos
- Falta de tipagem em interfaces públicas
- Comentários desatualizados ou enganosos
- Magic numbers sem constantes nomeadas
- Dead code (código inalcançável ou não utilizado)

### Camada 5: Boas Práticas do Stack

**Python:**

- Uso de type hints
- Conformidade com PEP 8 / black / ruff
- Uso correto de context managers
- Dataclasses/Pydantic vs dicts soltos
- Async onde aplicável

**TypeScript/React:**

- Tipagem estrita (sem `any`)
- Hooks rules
- Memoização onde necessário
- Error boundaries
- Acessibilidade (a11y)

**Geral:**

- Princípio da menor surpresa
- Single Responsibility
- Fail fast
- Defensive programming em boundaries (APIs, inputs)

## Formato de Saída

Sempre estruture o resultado assim:

````
## RESUMO
X vulnerabilidades encontradas: N críticas, N altas, N médias, N baixas.

## VULNERABILIDADES

### 🔴 CRÍTICA — [Título descritivo]
- Arquivo: `path/to/file.py`, linha X
- Problema: [Descrição clara do risco]
- Impacto: [O que pode acontecer se explorado/ativado]
- Fix:
```[linguagem]
// código corrigido
````

- Referência: [CWE/OWASP se aplicável]

### 🟠 ALTA — [Título descritivo]

...

### 🟡 MÉDIA — [Título descritivo]

...

### 🔵 BAIXA — [Título descritivo]

...

## PONTOS POSITIVOS

- [O que está bem feito — reconhecer boas práticas já aplicadas]

## RECOMENDAÇÕES GERAIS

- [Melhorias estruturais que não são bugs mas melhorariam o código]

```

## Classificação de Criticidade

| Nível | Critério | Exemplo |
|-------|----------|---------|
| 🔴 Crítica | Pode ser explorado remotamente, causa vazamento de dados ou indisponibilidade | SQL injection, secret exposto, auth bypass |
| 🟠 Alta | Causa bug em produção ou perda de dados em cenários reais | Race condition, recurso não liberado, erro silenciado em operação crítica |
| 🟡 Média | Degrada performance ou dificulta manutenção significativamente | Query N+1, O(n²) evitável, função de 200 linhas |
| 🔵 Baixa | Melhoria de qualidade sem risco imediato | Naming ruim, falta de type hint, magic number |

## Regras de Eficiência

- Não reporte problemas de estilo que um linter resolve automaticamente (black, ruff, eslint)
- Se o projeto tem linter configurado, assuma que estilo já é tratado
- Foque em lógica, segurança e arquitetura — o que ferramentas automáticas NÃO pegam
- Limite o relatório a no máximo 10 itens mais relevantes (não despeje 50 warnings)
- Se o código está bom, diga "código sólido, sem vulnerabilidades críticas encontradas" — não invente problemas

## Contexto de Análise

Antes de revisar, considere:
- Qual é o ambiente? (dev, staging, prod)
- É código de API pública ou lógica interna?
- Qual o nível de confiança nos inputs? (usuário externo vs. sistema interno)
- Existe autenticação/autorização antes deste ponto?
- Qual o volume esperado? (10 req/dia vs. 10K req/s)

Isso muda a criticidade. Um SQL injection numa rota pública é crítico. Num script interno de migração one-shot, é baixo.

## Exemplo de Uso

**Input:** "Revise este endpoint de autenticação"

**Análise esperada:**
- Verificar se JWT é validado corretamente
- Checar se secrets estão em variáveis de ambiente (não hardcoded)
- Verificar timing attacks em comparação de tokens
- Checar rate limiting
- Verificar se password hashing usa bcrypt/argon2 (não MD5/SHA)
- Checar se tokens expiram

## Anti-Patterns (o que NÃO fazer na revisão)

- Não seja pedante com estilo quando há linter configurado
- Não sugira refatorações massivas sem justificativa de impacto
- Não reporte "poderia usar list comprehension" como vulnerabilidade
- Não invente cenários improváveis para inflar o relatório
- Não ignore o contexto do projeto para aplicar regras genéricas
```
