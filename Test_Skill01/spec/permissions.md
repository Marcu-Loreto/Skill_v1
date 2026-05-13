# Permissões e Controle de Acesso — Skill_Presentation

> Gerado pelo Detetive em 2026-05-11
> Escala de confiança: 🟢 CONFIRMADO | 🟡 INFERIDO | 🔴 LACUNA

---

## Resumo

O sistema **não possui controle de acesso**. Não há autenticação, autorização, papéis de usuário ou qualquer mecanismo de RBAC/ACL implementado.

---

## Evidências 🟢

| Aspecto              | Status     | Evidência                                                      |
| -------------------- | ---------- | -------------------------------------------------------------- |
| Login / Autenticação | ❌ Ausente | Nenhum middleware de auth, nenhuma tela de login               |
| Papéis de usuário    | ❌ Ausente | Nenhum enum de roles, nenhum campo `role` em qualquer entidade |
| Proteção de rotas    | ❌ Ausente | Streamlit não tem conceito de rotas protegidas                 |
| API keys do usuário  | ❌ Ausente | Keys são do servidor (.env), não por usuário                   |
| Multi-tenancy        | ❌ Ausente | Todos os templates e exports são compartilhados                |
| Rate limiting        | ❌ Ausente | Nenhum throttle por IP ou sessão                               |
| Auditoria de ações   | ❌ Ausente | Nenhum log de quem gerou o quê                                 |

---

## Implicações 🟡

1. **Qualquer pessoa com acesso à URL pode gerar apresentações** — consumindo créditos de API (OpenAI, Tavily)
2. **Templates são globais** — um usuário pode deletar templates de outro
3. **Exports são acessíveis por qualquer sessão** — pasta `exports/` sem isolamento
4. **Sem limite de uso** — possível abuso de API keys compartilhadas

---

## Recomendações 🔴

| Prioridade | Recomendação                                                                      |
| ---------- | --------------------------------------------------------------------------------- |
| Alta       | Implementar autenticação básica (mesmo que simples: senha compartilhada ou OAuth) |
| Alta       | Rate limiting por sessão/IP para proteger créditos de API                         |
| Média      | Isolamento de exports por sessão ou usuário                                       |
| Média      | Proteção de templates (owner-only delete)                                         |
| Baixa      | Auditoria de gerações (quem, quando, tema, custo estimado)                        |

> **Nota**: Para um protótipo/MVP interno, a ausência de auth pode ser aceitável. Para deploy público, é uma lacuna crítica.
