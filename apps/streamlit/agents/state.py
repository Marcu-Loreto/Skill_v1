"""
State definition for the Presentation Generator pipeline.
Single source of truth passed between all agent nodes.
"""

from typing import TypedDict, Literal


class ResearchResult(TypedDict):
    """A single research finding from web search."""
    title: str
    source: str
    url: str
    snippet: str
    date: str  # publication date if available


class SlideContent(TypedDict):
    """Content for a single slide."""
    slide_number: int
    title: str
    subtitle: str
    content: list[str]  # bullet points or paragraphs
    notes: str  # speaker notes


class PresentationState(TypedDict):
    """Main state for the presentation generation pipeline."""
    # Input
    tema: str
    publico: str
    tom: str
    num_slides: int
    template: str
    formato_saida: list[str]
    incluir_referencias: bool
    incluir_agenda: bool
    mode: Literal["free", "proposal"]

    # Research phase
    research_queries: list[str]
    research_results: list[ResearchResult]
    selected_data: list[ResearchResult]  # filtered best results

    # Structure phase
    slide_titles: list[str]
    slides: list[SlideContent]

    # Generation phase
    html_content: str
    html_path: str

    # Conversion phase
    pptx_path: str

    # Validation
    is_valid: bool
    error: str
