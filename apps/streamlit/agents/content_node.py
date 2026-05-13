"""
Content Generation Node — Professional writing for each slide.
Generates structured content (title, bullets, notes) for every slide.

Model strategy: GPT-4o (complex task — quality writing with data integration)
"""

from typing import Any


CONTENT_SYSTEM_PROMPT = None  # Loaded from file at runtime


def _get_content_system_prompt() -> str:
    """Load content agent system prompt from file."""
    from agents.prompt_loader import load_prompt
    return load_prompt("content_agent")


def build_content_prompt(state: dict) -> str:
    """Build prompt for content generation."""
    tema = state.get("tema", "")
    publico = state.get("publico", "")
    tom = state.get("tom", "")
    slide_titles = state.get("slide_titles", [])
    research_results = state.get("selected_data", [])

    # Format research data
    research_context = ""
    if research_results:
        research_context = "\nDADOS DISPONÍVEIS PARA USAR NOS SLIDES:\n"
        for i, r in enumerate(research_results[:5], 1):
            research_context += f"\n[{i}] Fonte: {r.get('source', 'N/A')}\n"
            research_context += f"    Título: {r.get('title', '')}\n"
            research_context += f"    Dados: {r.get('snippet', '')[:200]}\n"
            if r.get("url"):
                research_context += f"    URL: {r.get('url', '')}\n"

    # Format slide titles
    slides_list = "\n".join(f"{i+1}. {t}" for i, t in enumerate(slide_titles))

    return f"""TEMA DA APRESENTAÇÃO: {tema}
PÚBLICO-ALVO: {publico}
TOM: {tom}
{research_context}

SLIDES A GERAR CONTEÚDO:
{slides_list}

Gere o conteúdo completo para TODOS os {len(slide_titles)} slides acima.
Use os dados pesquisados quando relevante. Cite a fonte entre parênteses.
Siga o formato ---SLIDE--- / ---FIM--- para cada slide.
"""


def parse_content_response(response: str, slide_titles: list[str]) -> list[dict]:
    """Parse LLM response into structured slide content."""
    import re

    slides = []
    # Split by slide markers
    slide_blocks = re.split(r"---SLIDE---", response)

    for block in slide_blocks:
        block = block.strip()
        if not block or "---FIM---" not in block and len(block) < 20:
            continue

        # Remove end marker
        block = block.replace("---FIM---", "").strip()

        slide = {
            "title": "",
            "subtitle": "",
            "content": [],
            "notes": "",
        }

        lines = block.split("\n")
        current_section = None

        for line in lines:
            line = line.strip()
            if not line:
                continue

            if line.upper().startswith("TÍTULO:") or line.upper().startswith("TITULO:"):
                slide["title"] = re.sub(r"^T[ÍI]TULO:\s*", "", line, flags=re.IGNORECASE).strip()
                current_section = None
            elif line.upper().startswith("SUBTÍTULO:") or line.upper().startswith("SUBTITULO:"):
                slide["subtitle"] = re.sub(
                    r"^SUBT[ÍI]TULO:\s*", "", line, flags=re.IGNORECASE
                ).strip()
                current_section = None
            elif line.upper().startswith("CONTEÚDO:") or line.upper().startswith("CONTEUDO:"):
                current_section = "content"
            elif line.upper().startswith("NOTAS:"):
                slide["notes"] = re.sub(r"^NOTAS:\s*", "", line, flags=re.IGNORECASE).strip()
                current_section = "notes"
            elif current_section == "content":
                # Remove bullet markers
                bullet = re.sub(r"^[-•→▸]\s*", "", line).strip()
                if bullet:
                    slide["content"].append(bullet)
            elif current_section == "notes":
                slide["notes"] += " " + line

        if slide["title"] or slide["content"]:
            slides.append(slide)

    # Ensure we have content for all titles
    while len(slides) < len(slide_titles):
        idx = len(slides)
        title = slide_titles[idx] if idx < len(slide_titles) else f"Slide {idx + 1}"
        slides.append({
            "title": title,
            "subtitle": "",
            "content": ["Conteúdo a ser desenvolvido"],
            "notes": "",
        })

    # Add slide numbers
    for i, slide in enumerate(slides):
        slide["slide_number"] = i + 1

    return slides


def generate_content_deterministic(state: dict) -> list[dict]:
    """
    Fallback: generate minimal content without LLM.
    Uses research snippets as bullet points.
    """
    slide_titles = state.get("slide_titles", [])
    research_results = state.get("selected_data", [])
    tema = state.get("tema", "")

    slides = []
    for i, title in enumerate(slide_titles):
        slide = {
            "slide_number": i + 1,
            "title": title,
            "subtitle": "",
            "content": [],
            "notes": "",
        }

        # First slide = cover
        if i == 0:
            slide["subtitle"] = tema if title != tema else ""
            slide["content"] = []
        # Use research data for middle slides
        elif i < len(slide_titles) - 1 and research_results:
            # Distribute research across slides
            data_idx = (i - 1) % len(research_results)
            r = research_results[data_idx]
            snippet = r.get("snippet", "")
            # Split snippet into bullet-sized chunks
            sentences = [s.strip() for s in snippet.split(".") if len(s.strip()) > 10]
            slide["content"] = sentences[:4]
            slide["notes"] = f"Fonte: {r.get('source', '')}"
        else:
            slide["content"] = ["Conteúdo a ser desenvolvido"]

        slides.append(slide)

    return slides


def content_node(state: dict) -> dict:
    """
    LangGraph node: Content Generation.
    Generates professional content for each slide.

    Uses GPT-4o (complex task — quality writing).
    Falls back to deterministic if no API key.

    Input: tema, publico, tom, slide_titles, selected_data
    Output: slides (list of SlideContent)
    """
    slide_titles = state.get("slide_titles", [])

    if not slide_titles:
        return {**state, "slides": [], "error": "Nenhum título de slide definido"}

    try:
        from config import get_settings
        from langchain_openai import ChatOpenAI

        settings = get_settings()

        if settings.has_openai:
            model_name = settings.get_model_for_task("complex")
            llm = ChatOpenAI(
                model=model_name,
                api_key=settings.openai_api_key,
                temperature=0.7,
                max_tokens=4000,
            )

            system_msg = _get_content_system_prompt()
            user_msg = build_content_prompt(state)

            from langchain_core.messages import SystemMessage, HumanMessage

            response = llm.invoke([
                SystemMessage(content=system_msg),
                HumanMessage(content=user_msg),
            ])

            slides = parse_content_response(response.content, slide_titles)
            return {**state, "slides": slides}

    except Exception:
        pass

    # Fallback: deterministic content
    slides = generate_content_deterministic(state)
    return {**state, "slides": slides}
