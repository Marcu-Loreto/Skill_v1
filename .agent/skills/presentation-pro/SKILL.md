---
name: presentation-pro
description: Gera apresentações profissionais completas sobre qualquer tema fornecido pelo usuário. Pesquisa dados reais em fontes acadêmicas e confiáveis, busca imagens reais de bancos de imagens, e produz slides estruturados em formato Markdown/HTML com visual profissional. Use esta skill sempre que o usuário pedir para criar apresentação, slides, pitch deck, deck de slides, apresentação corporativa, apresentação acadêmica, ou mencionar termos como "crie uma apresentação", "faça slides sobre", "monte um deck", "apresentação profissional", "slides para reunião", "apresentação para investidores".
---

# Presentation Pro — Gerador de Apresentações Profissionais

## Objetivo

Criar apresentações profissionais, visualmente atraentes e baseadas em dados reais sobre qualquer tema solicitado pelo usuário. A apresentação deve ser fundamentada em pesquisa de fontes confiáveis e incluir imagens relevantes.

## Fluxo de Trabalho

```
Tema do Usuário → Guardrails → Pesquisa Web → Estruturação → Busca de Imagens → Geração → Exportação
```

### Etapa 1: Validação de Conteúdo (Guardrails)

Antes de qualquer processamento, valide o tema contra as políticas de conteúdo. Se o tema violar as regras, recuse educadamente e explique o motivo.

### Etapa 2: Briefing

Colete do usuário (ou infira do contexto):

- Tema principal
- Público-alvo (executivos, acadêmico, técnico, geral)
- Tom desejado (formal, casual, inspiracional, técnico)
- Número aproximado de slides (padrão: 10-15)
- Formato de exportação preferido (Markdown, HTML, PPTX via python-pptx)

Se o usuário não especificar, use os padrões sensatos e prossiga.

### Etapa 3: Pesquisa de Conteúdo

Use web search para buscar dados reais. Priorize estas fontes:

**Fontes Acadêmicas e Confiáveis (prioridade):**

- Google Scholar / artigos científicos
- Relatórios de consultorias (McKinsey, Gartner, Deloitte, PwC)
- Dados governamentais (IBGE, Banco Central, IPEA)
- Organizações internacionais (OMS, ONU, Banco Mundial, OCDE)
- Publicações setoriais reconhecidas
- Statista, Our World in Data

**Critérios de qualidade:**

- Dados com data de publicação (preferir últimos 2 anos)
- Fontes com metodologia transparente
- Números verificáveis e citáveis
- Evitar blogs pessoais, fóruns, conteúdo sem autoria

**Para cada dado usado, registre:**

- Fonte original
- Data de publicação
- URL de referência

### Etapa 4: Estruturação dos Slides

Estruture a apresentação seguindo este framework:

```
Slide 1: Capa (título + subtítulo + imagem de impacto)
Slide 2: Agenda / Sumário
Slide 3-4: Contexto / Problema
Slide 5-8: Desenvolvimento (dados, análises, insights)
Slide 9-10: Casos / Exemplos reais
Slide 11-12: Recomendações / Próximos passos
Slide 13: Conclusão / Call-to-action
Slide 14: Referências
```

Adapte a quantidade e ordem conforme o tema e público.

**Princípios de design por slide:**

- Máximo 6 linhas de texto por slide
- Uma ideia principal por slide
- Dados em formato visual quando possível (bullets com números, comparações)
- Títulos de slide como afirmações, não como tópicos genéricos

### Etapa 5: Busca de Imagens

Para cada slide que necessite de imagem, busque imagens reais usando web search nos seguintes bancos:

**Bancos de imagens gratuitos (prioridade):**

- Unsplash (https://unsplash.com)
- Pexels (https://pexels.com)
- Pixabay (https://pixabay.com)

**Estratégia de busca:**

- Use termos em inglês para maior variedade de resultados
- Busque imagens contextuais (não genéricas)
- Prefira fotos com pessoas reais e cenários autênticos
- Para dados/gráficos, descreva o gráfico a ser criado

**Para cada imagem, forneça:**

- URL direta da imagem
- Crédito do fotógrafo/fonte
- Descrição alt-text para acessibilidade

Se não encontrar imagem adequada, forneça uma descrição detalhada da imagem ideal para o usuário gerar via IA ou buscar manualmente.

### Etapa 6: Geração da Apresentação

Gere a apresentação no formato solicitado:

**Formato padrão: Markdown estruturado**

```markdown
---
title: "Título da Apresentação"
author: "[Nome]"
date: "2026"
theme: professional
---

# Slide 1: Título

![Imagem de capa](url_da_imagem)
_Crédito: Fotógrafo / Banco_

## Título Impactante da Apresentação

### Subtítulo contextual

---

# Slide 2: Agenda

1. Contexto atual
2. Dados e análise
3. Insights principais
4. Recomendações

---
```

**Formato alternativo: HTML (para visualização direta)**

Se o usuário preferir visualização imediata, gere um arquivo HTML standalone com:

- CSS embutido com design profissional
- Navegação entre slides (setas)
- Imagens incorporadas via URL
- Responsivo para projeção
- **TEMA PADRÃO: Dark mode** (fundo escuro #0a0e1a / #0f172a, texto claro #f1f5f9, acentos em cyan #22d3ee). Só use tema claro (fundo branco) se o usuário solicitar explicitamente.

### Etapa 7: Referências e Citações

Sempre inclua um slide final com todas as referências no formato:

```
[1] Autor/Organização. "Título". Fonte, Data. URL
[2] ...
```

## Guardrails — Política de Conteúdo

### Temas BLOQUEADOS (recuse imediatamente):

- Conteúdo sexual ou pornográfico
- Discurso de ódio (racial, étnico, religioso, de gênero, orientação sexual)
- Apologia à violência ou terrorismo
- Conteúdo que promova discriminação contra grupos protegidos
- Desinformação intencional sobre saúde pública
- Instruções para atividades ilegais
- Conteúdo que explore ou prejudique menores
- Propaganda extremista ou supremacista

### Resposta padrão para bloqueio:

> "Não posso criar apresentações sobre este tema pois viola as políticas de conteúdo seguro. Posso ajudar com apresentações sobre temas profissionais, acadêmicos, corporativos, educacionais ou informativos. Deseja sugerir outro tema?"

### Temas PERMITIDOS com cuidado:

- Saúde e medicina (usar apenas fontes científicas)
- Política e economia (manter neutralidade, apresentar múltiplas perspectivas)
- Temas controversos legítimos (apresentar dados, não opinião)

## Padrões de Qualidade

### Texto

- Português do Brasil (pt-BR) para conteúdo
- Frases curtas e diretas
- Sem jargão desnecessário (adaptar ao público)
- Dados sempre com fonte e data

### Visual

- **Dark mode por padrão** — fundo escuro (#0a0e1a ou #0f172a), texto claro (#f1f5f9), acentos em cyan (#22d3ee). Só gerar tema claro se o usuário pedir explicitamente.
- Consistência visual entre slides
- Paleta de cores coerente (sugerir com base no tema)
- Hierarquia tipográfica clara (título > subtítulo > corpo)
- Espaço em branco generoso

### Dados

- Mínimo 3 dados/estatísticas de fontes confiáveis por apresentação
- Todos os números com fonte citada
- Preferir dados recentes (últimos 2 anos)
- Contextualizar números (comparações, tendências)

## Exemplo de Uso

**Entrada:** "Crie uma apresentação sobre o impacto da IA no mercado de trabalho brasileiro"

**Processo:**

1. ✅ Tema validado (não viola guardrails)
2. Pesquisa: buscar dados IBGE, McKinsey, WEF sobre automação e emprego no Brasil
3. Estrutura: 12 slides (contexto global → dados Brasil → setores impactados → habilidades do futuro → recomendações)
4. Imagens: buscar fotos de profissionais, tecnologia, indústria brasileira
5. Gerar: Markdown estruturado com imagens e referências

## Dicas de Uso

- Quanto mais contexto o usuário der (público, objetivo, tom), melhor o resultado
- Para apresentações técnicas, incluir mais dados e menos texto narrativo
- Para pitch decks, focar em problema → solução → mercado → tração → ask
- Para acadêmicas, seguir estrutura IMRAD adaptada e citar metodologia
