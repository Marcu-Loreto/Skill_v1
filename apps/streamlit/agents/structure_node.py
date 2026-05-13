"""
Structure Node — Logical slide organization.
Decides slide titles and order based on theme, audience, and research data.

Model strategy: MiniMax M2.5 (simple task — organizing structure)
Fallback: deterministic template if no LLM available.
"""

from typing import Any


# --- Slide frameworks by presentation type ---
FRAMEWORK_FREE = [
    "Capa",
    "Agenda",
    "Contexto / Cenário Atual",
    "Dados e Evidências",
    "Análise Aprofundada",
    "Casos e Exemplos",
    "Insights Principais",
    "Recomendações",
    "Próximos Passos",
    "Conclusão",
    "Referências",
]

FRAMEWORK_PROPOSAL = [
    "Capa",
    "Contexto / Problema",
    "Solução Proposta",
    "Diferenciais",
    "Escopo do Projeto",
    "Tecnologias",
    "Etapas de Desenvolvimento",
    "Cronograma",
    "Equipe",
    "Investimento",
    "Próximos Passos",
]


def build_structure_prompt(state: dict) -> str:
    """Build the prompt for the LLM to generate slide structure."""
    from agents.prompt_loader import load_prompt

    tema = state.get("tema", "")
    publico = state.get("publico", "")
    tom = state.get("tom", "")
    num_slides = state.get("num_slides", 12)
    research_results = state.get("selected_data", [])

    # Load system prompt from file
    system_prompt = load_prompt("structure_agent")

    # Format research data for context
    research_context = ""
    if research_results:
        research_context = "\n\nDADOS PESQUISADOS DISPONÍVEIS:\n"
        for i, r in enumerate(research_results[:5], 1):
            research_context += f"{i}. [{r.get('source', '')}] {r.get('title', '')}\n"
            research_context += f"   {r.get('snippet', '')[:150]}\n"

    user_prompt = f"""TEMA: {tema}
PÚBLICO-ALVO: {publico}
TOM: {tom}
NÚMERO DE SLIDES: {num_slides}
{research_context}

Gere exatamente {num_slides} títulos de slides seguindo as regras do sistema.
"""

    return system_prompt + "\n\n---\n\n" + user_prompt


def parse_structure_response(response: str, num_slides: int) -> list[str]:
    """Parse LLM response into list of slide titles."""
    import re

    lines = response.strip().split("\n")
    titles = []

    for line in lines:
        # Remove numbering (1. , 2. , etc.)
        cleaned = re.sub(r"^\d+[\.\)]\s*", "", line.strip())
        # Remove markdown formatting
        cleaned = re.sub(r"[\*\#\[\]]", "", cleaned).strip()
        if cleaned and len(cleaned) > 2:
            titles.append(cleaned)

    # Ensure we have the right number
    if len(titles) > num_slides:
        titles = titles[:num_slides]
    elif len(titles) < num_slides:
        # Pad with generic titles
        while len(titles) < num_slides:
            titles.append(f"Slide {len(titles) + 1}")

    return titles


def generate_structure_deterministic(state: dict) -> list[str]:
    """
    Fallback: generate structure without LLM using framework templates.
    Adapts the framework to the requested number of slides.
    """
    num_slides = state.get("num_slides", 12)
    mode = state.get("mode", "free")
    tema = state.get("tema", "Apresentação")
    incluir_agenda = state.get("incluir_agenda", True)
    incluir_referencias = state.get("incluir_referencias", True)

    if mode == "proposal":
        framework = FRAMEWORK_PROPOSAL.copy()
    else:
        framework = FRAMEWORK_FREE.copy()

    # Remove optional slides if not needed
    if not incluir_agenda and "Agenda" in framework:
        framework.remove("Agenda")
    if not incluir_referencias and "Referências" in framework:
        framework.remove("Referências")

    # Adjust to target number of slides
    if len(framework) > num_slides:
        # Remove middle slides (keep first 2 and last 2)
        keep_start = 2
        keep_end = 2
        middle_needed = num_slides - keep_start - keep_end
        middle = framework[keep_start:-keep_end][:middle_needed]
        framework = framework[:keep_start] + middle + framework[-keep_end:]
    elif len(framework) < num_slides:
        # Add development slides
        extra_needed = num_slides - len(framework)
        insert_pos = len(framework) // 2
        for i in range(extra_needed):
            framework.insert(insert_pos + i, f"Desenvolvimento — Parte {i + 1}")

    # Replace "Capa" with actual theme
    if framework and framework[0] == "Capa":
        framework[0] = tema

    return framework[:num_slides]


def structure_node(state: dict) -> dict:
    """
    LangGraph node: Structure.
    Generates the logical slide organization.

    Uses LLM (MiniMax) if available, otherwise deterministic fallback.

    Input: tema, publico, tom, num_slides, selected_data
    Output: slide_titles
    """
    try:
        from config import get_settings
        from langchain_openai import ChatOpenAI

        settings = get_settings()

        if settings.has_openai:
            model_name = settings.get_model_for_task("simple")
            llm = ChatOpenAI(
                model=model_name,
                api_key=settings.openai_api_key,
                temperature=0.7,
                max_tokens=1000,
            )

            prompt = build_structure_prompt(state)
            response = llm.invoke(prompt)
            titles = parse_structure_response(response.content, state.get("num_slides", 12))

            return {**state, "slide_titles": titles}

    except Exception:
        pass

    # Fallback: deterministic structure
    titles = generate_structure_deterministic(state)
    return {**state, "slide_titles": titles}
