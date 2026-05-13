# Fluxograma — Config & Model Selection

> Gerado pelo Arqueólogo em 2026-05-11

## Carregamento de Configuração

```mermaid
flowchart TD
    A[Importa config.py] --> B[load_dotenv do .env]
    B --> C[Instancia Settings]
    C --> D[@lru_cache get_settings]
    D --> E[Singleton disponível]
```

## Seleção de Modelo (Implementação Real)

```mermaid
flowchart TD
    A[get_model_for_task] --> B{strategy?}
    B -->|simple| C[gpt-4o-mini]
    B -->|complex| C
    B -->|auto| C
    C --> D[Retorna gpt-4o-mini sempre]
```

## Seleção de Modelo (Design Pretendido — não implementado)

```mermaid
flowchart TD
    A[get_model_for_task] --> B{strategy?}
    B -->|simple| C[minimax-m2.5]
    B -->|complex| D[gpt-4o]
    B -->|auto| E{complexity?}
    E -->|simple| C
    E -->|complex| D
```
