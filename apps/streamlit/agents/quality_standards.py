"""
Output Quality Standards — Enforced rules for presentation content.

Standards:
- Language: pt-BR (Português do Brasil)
- Max 6 lines/bullets per slide
- Citations with source and date
- Format: 16:9 widescreen (13.333 x 7.5 inches)
- Titles as assertions (not generic topics)
- Data always with source attribution
"""

import re
from typing import Any


# --- Quality Constants ---
MAX_BULLETS_PER_SLIDE = 6
MAX_WORDS_PER_BULLET = 18
SLIDE_WIDTH_INCHES = 13.333
SLIDE_HEIGHT_INCHES = 7.5
ASPECT_RATIO = "16:9"
LANGUAGE = "pt-BR"

# Title patterns to avoid (too generic)
GENERIC_TITLE_PATTERNS = [
    r"^slide \d+$",
    r"^introdução$",
    r"^conclusão$",
    r"^desenvolvimento$",
    r"^conteúdo$",
    r"^informações$",
    r"^dados$",
    r"^overview$",
    r"^introduction$",
]


def enforce_bullet_limit(slides: list[dict], max_bullets: int = MAX_BULLETS_PER_SLIDE) -> list[dict]:
    """
    Enforce maximum bullets per slide.
    Truncates excess bullets and adds '...' indicator.
    """
    for slide in slides:
        content = slide.get("content", [])
        if len(content) > max_bullets:
            slide["content"] = content[:max_bullets - 1] + [
                f"(+{len(content) - max_bullets + 1} itens adicionais)"
            ]
    return slides


def enforce_bullet_length(slides: list[dict], max_words: int = MAX_WORDS_PER_BULLET) -> list[dict]:
    """
    Enforce maximum words per bullet point.
    Truncates long bullets with ellipsis.
    """
    for slide in slides:
        trimmed_content = []
        for bullet in slide.get("content", []):
            words = bullet.split()
            if len(words) > max_words:
                trimmed = " ".join(words[:max_words]) + "..."
                trimmed_content.append(trimmed)
            else:
                trimmed_content.append(bullet)
        slide["content"] = trimmed_content
    return slides


def check_citations(slides: list[dict]) -> dict:
    """
    Check if data claims have source citations.
    Returns report with slides that have uncited data.
    """
    citation_patterns = [
        r"\(.*?\d{4}\)",           # (Source, 2024)
        r"\(.*?20\d{2}\)",         # (Source, 20XX)
        r"Fonte:.*",              # Fonte: ...
        r"Source:.*",             # Source: ...
        r"\[.*?\]",               # [Source]
    ]

    data_patterns = [
        r"\d+%",                  # percentages
        r"R\$\s*[\d.,]+",         # BRL values
        r"\$\s*[\d.,]+",          # USD values
        r"\d+\s*(milhões|bilhões|mil)",  # large numbers
    ]

    uncited_slides = []

    for slide in slides:
        for bullet in slide.get("content", []):
            has_data = any(re.search(p, bullet) for p in data_patterns)
            has_citation = any(re.search(p, bullet) for p in citation_patterns)

            if has_data and not has_citation:
                uncited_slides.append({
                    "slide": slide.get("slide_number", 0),
                    "title": slide.get("title", ""),
                    "bullet": bullet,
                })
                break  # One per slide is enough

    return {
        "total_slides": len(slides),
        "slides_with_uncited_data": len(uncited_slides),
        "details": uncited_slides,
        "citation_rate": 1 - (len(uncited_slides) / max(len(slides), 1)),
    }


def check_title_quality(slides: list[dict]) -> list[str]:
    """
    Check for generic/weak slide titles.
    Returns list of warnings.
    """
    warnings = []

    for slide in slides:
        title = slide.get("title", "").lower().strip()
        for pattern in GENERIC_TITLE_PATTERNS:
            if re.match(pattern, title):
                warnings.append(
                    f"Slide {slide.get('slide_number', '?')}: "
                    f"título genérico '{slide.get('title', '')}' — "
                    f"use uma afirmação específica"
                )
                break

    return warnings


def apply_quality_standards(slides: list[dict]) -> dict:
    """
    Apply all quality standards to slides.
    Returns modified slides + quality report.
    """
    # Enforce limits
    slides = enforce_bullet_limit(slides)
    slides = enforce_bullet_length(slides)

    # Check quality
    citation_report = check_citations(slides)
    title_warnings = check_title_quality(slides)

    # Quality score (0-100)
    score = 100
    score -= len(title_warnings) * 5  # -5 per generic title
    score -= citation_report["slides_with_uncited_data"] * 3  # -3 per uncited slide
    score = max(0, min(100, score))

    return {
        "slides": slides,
        "quality_score": score,
        "citation_report": citation_report,
        "title_warnings": title_warnings,
        "standards_applied": {
            "max_bullets_per_slide": MAX_BULLETS_PER_SLIDE,
            "max_words_per_bullet": MAX_WORDS_PER_BULLET,
            "format": ASPECT_RATIO,
            "language": LANGUAGE,
            "slide_dimensions": f"{SLIDE_WIDTH_INCHES} x {SLIDE_HEIGHT_INCHES} inches",
        },
    }


# --- Quality prompt injection for LLM nodes ---
QUALITY_PROMPT_SUFFIX = """

PADRÕES DE QUALIDADE OBRIGATÓRIOS:
- Idioma: Português do Brasil (pt-BR)
- Máximo 6 bullets por slide
- Máximo 18 palavras por bullet
- Dados SEMPRE com fonte e ano entre parênteses: (Fonte, Ano)
- Títulos como afirmações específicas, NUNCA genéricos como "Introdução" ou "Dados"
- Formato: 16:9 widescreen
- Sem jargão desnecessário — adaptar ao público-alvo
"""
