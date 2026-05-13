"""
Research Node — Web search from reliable sources.
Searches for real data relevant to the presentation theme.
Uses Tavily for web search (or fallback to DuckDuckGo).

Model strategy: MiniMax M2.5 (simple task — filtering/ranking results)
"""

import re
from typing import Any

from langchain_core.messages import SystemMessage, HumanMessage


# --- Reliable source domains (prioritized) ---
TRUSTED_DOMAINS = [
    # Consultorias
    "mckinsey.com", "deloitte.com", "bcg.com", "pwc.com",
    "gartner.com", "accenture.com", "bain.com",
    # Organizações internacionais
    "worldbank.org", "weforum.org", "oecd.org", "un.org",
    "who.int", "imf.org",
    # Governo Brasil
    "gov.br", "ibge.gov.br", "ipea.gov.br", "bndes.gov.br",
    # Dados e pesquisa
    "statista.com", "ourworldindata.org", "nature.com",
    "sciencedirect.com", "scholar.google.com",
    # Tech research
    "idc.com", "forrester.com", "salesforce.com",
    "google.com/blog", "microsoft.com",
]

# Domains to avoid
BLOCKED_DOMAINS = [
    "pinterest.com", "facebook.com", "instagram.com",
    "tiktok.com", "reddit.com", "quora.com",
    "medium.com",  # often low quality
]


def generate_search_queries(tema: str, publico: str, num_queries: int = 3) -> list[str]:
    """
    Generate search queries based on the theme.
    Uses simple heuristics — no LLM needed for this.
    """
    # Base query
    queries = [tema]

    # Add data-focused query
    queries.append(f"{tema} dados estatísticas 2025 2026")

    # Add English query for broader results
    # Simple keyword extraction (no LLM needed)
    clean_tema = re.sub(r"[^\w\s]", "", tema)
    words = [w for w in clean_tema.split() if len(w) > 3]
    if words:
        en_query = " ".join(words[:5]) + " statistics report 2025"
        queries.append(en_query)

    return queries[:num_queries]


def is_trusted_source(url: str) -> bool:
    """Check if URL is from a trusted domain."""
    url_lower = url.lower()
    for domain in BLOCKED_DOMAINS:
        if domain in url_lower:
            return False
    for domain in TRUSTED_DOMAINS:
        if domain in url_lower:
            return True
    # Allow other domains but with lower priority
    return False


def search_tavily(query: str, max_results: int = 5) -> list[dict]:
    """
    Search using Tavily API.
    Returns list of results with title, url, content, score.
    """
    try:
        from tavily import TavilyClient
        from config import get_settings

        settings = get_settings()
        if not settings.has_tavily:
            return []

        client = TavilyClient(api_key=settings.tavily_api_key)
        response = client.search(
            query=query,
            max_results=max_results,
            search_depth="advanced",
            include_domains=[d for d in TRUSTED_DOMAINS[:10]],
        )

        results = []
        for item in response.get("results", []):
            results.append({
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "snippet": item.get("content", "")[:300],
                "score": item.get("score", 0),
                "source": extract_domain(item.get("url", "")),
                "date": "",  # Tavily doesn't always return dates
            })
        return results

    except Exception:
        return []


def search_duckduckgo(query: str, max_results: int = 5) -> list[dict]:
    """
    Fallback search using DuckDuckGo (no API key needed).
    """
    try:
        from langchain_community.utilities import DuckDuckGoSearchAPIWrapper

        ddg = DuckDuckGoSearchAPIWrapper(max_results=max_results)
        raw_results = ddg.results(query, max_results=max_results)

        results = []
        for item in raw_results:
            results.append({
                "title": item.get("title", ""),
                "url": item.get("link", ""),
                "snippet": item.get("snippet", "")[:300],
                "score": 0.5,  # no score from DDG
                "source": extract_domain(item.get("link", "")),
                "date": "",
            })
        return results

    except Exception:
        return []


def extract_domain(url: str) -> str:
    """Extract clean domain from URL."""
    try:
        from urllib.parse import urlparse
        parsed = urlparse(url)
        domain = parsed.netloc.replace("www.", "")
        return domain
    except Exception:
        return url


def filter_and_rank_results(
    results: list[dict], max_results: int = 8
) -> list[dict]:
    """
    Filter and rank results by relevance and source trust.
    No LLM needed — deterministic scoring.
    """
    scored = []
    seen_domains = set()

    for r in results:
        score = r.get("score", 0.5)

        # Boost trusted sources
        if is_trusted_source(r.get("url", "")):
            score += 0.3

        # Penalize duplicates from same domain
        domain = r.get("source", "")
        if domain in seen_domains:
            score -= 0.2
        seen_domains.add(domain)

        # Penalize empty snippets
        if not r.get("snippet"):
            score -= 0.3

        # Penalize very short snippets
        if len(r.get("snippet", "")) < 50:
            score -= 0.1

        scored.append({**r, "final_score": score})

    # Sort by score descending
    scored.sort(key=lambda x: x["final_score"], reverse=True)

    # Return top results
    return scored[:max_results]


def research_node(state: dict) -> dict:
    """
    LangGraph node: Research.
    Searches the web for relevant data about the presentation theme.

    Input state keys: tema, publico
    Output state keys: research_queries, research_results, selected_data
    """
    tema = state.get("tema", "")
    publico = state.get("publico", "")

    if not tema:
        return {
            **state,
            "research_queries": [],
            "research_results": [],
            "selected_data": [],
            "error": "Tema não fornecido",
        }

    # Step 1: Generate queries (no LLM — heuristic)
    queries = generate_search_queries(tema, publico)

    # Step 2: Execute searches
    all_results = []

    for query in queries:
        # Try Tavily first (better quality)
        results = search_tavily(query, max_results=5)

        # Fallback to DuckDuckGo
        if not results:
            results = search_duckduckgo(query, max_results=5)

        all_results.extend(results)

    # Step 3: Deduplicate by URL
    seen_urls = set()
    unique_results = []
    for r in all_results:
        url = r.get("url", "")
        if url and url not in seen_urls:
            seen_urls.add(url)
            unique_results.append(r)

    # Step 4: Filter and rank (no LLM — deterministic)
    selected = filter_and_rank_results(unique_results, max_results=8)

    # Convert to ResearchResult format
    research_results = [
        {
            "title": r.get("title", ""),
            "source": r.get("source", ""),
            "url": r.get("url", ""),
            "snippet": r.get("snippet", ""),
            "date": r.get("date", ""),
        }
        for r in selected
    ]

    return {
        **state,
        "research_queries": queries,
        "research_results": research_results,
        "selected_data": research_results[:5],  # Top 5 for slide content
    }
