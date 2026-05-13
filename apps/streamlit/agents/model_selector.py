"""
Model Selection Optimization — Cost-effective model assignment per pipeline node.

Strategy:
- Research: No LLM (web search + deterministic filtering)
- Structure: MiniMax M2.5 / gpt-4o-mini (simple — organizing titles)
- Content: GPT-4o (complex — quality writing with data integration)
- HTML: No LLM (template rendering)
- PPTX: No LLM (file conversion)
- Validation: No LLM (file checks)

Cost per presentation (estimated):
- All GPT-4o: ~$0.20-0.30
- Optimized mix: ~$0.05-0.10 (60% savings)
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class TaskComplexity(Enum):
    """Task complexity levels for model selection."""
    NONE = "none"        # No LLM needed
    SIMPLE = "simple"    # MiniMax M2.5 or gpt-4o-mini
    COMPLEX = "complex"  # GPT-4o


@dataclass
class NodeModelConfig:
    """Model configuration for a pipeline node."""
    node_name: str
    complexity: TaskComplexity
    model: str
    max_tokens: int
    temperature: float
    estimated_cost_usd: float  # per invocation


# --- Pipeline node model assignments ---
NODE_CONFIGS: dict[str, NodeModelConfig] = {
    "research": NodeModelConfig(
        node_name="research",
        complexity=TaskComplexity.NONE,
        model="none",
        max_tokens=0,
        temperature=0,
        estimated_cost_usd=0.0,
    ),
    "structure": NodeModelConfig(
        node_name="structure",
        complexity=TaskComplexity.SIMPLE,
        model="gpt-4o-mini",  # or minimax-m2.5
        max_tokens=1000,
        temperature=0.7,
        estimated_cost_usd=0.002,
    ),
    "content": NodeModelConfig(
        node_name="content",
        complexity=TaskComplexity.COMPLEX,
        model="gpt-4o-mini",
        max_tokens=4000,
        temperature=0.7,
        estimated_cost_usd=0.005,
    ),
    "html_generation": NodeModelConfig(
        node_name="html_generation",
        complexity=TaskComplexity.NONE,
        model="none",
        max_tokens=0,
        temperature=0,
        estimated_cost_usd=0.0,
    ),
    "pptx_conversion": NodeModelConfig(
        node_name="pptx_conversion",
        complexity=TaskComplexity.NONE,
        model="none",
        max_tokens=0,
        temperature=0,
        estimated_cost_usd=0.0,
    ),
    "validation": NodeModelConfig(
        node_name="validation",
        complexity=TaskComplexity.NONE,
        model="none",
        max_tokens=0,
        temperature=0,
        estimated_cost_usd=0.0,
    ),
}


def get_node_config(node_name: str) -> NodeModelConfig:
    """Get model configuration for a specific pipeline node."""
    return NODE_CONFIGS.get(node_name, NODE_CONFIGS["validation"])


def get_model_for_node(node_name: str) -> Optional[str]:
    """Get the model name for a node. Returns None if no LLM needed."""
    config = get_node_config(node_name)
    if config.complexity == TaskComplexity.NONE:
        return None

    # Apply settings override
    try:
        from config import get_settings
        settings = get_settings()
        return settings.get_model_for_task(config.complexity.value)
    except Exception:
        return config.model


def estimate_pipeline_cost() -> dict:
    """Estimate total cost for one full pipeline execution."""
    total = sum(c.estimated_cost_usd for c in NODE_CONFIGS.values())
    breakdown = {
        name: f"${c.estimated_cost_usd:.3f}" for name, c in NODE_CONFIGS.items()
    }
    return {
        "total_estimated_usd": f"${total:.3f}",
        "breakdown": breakdown,
        "nodes_using_llm": [
            name for name, c in NODE_CONFIGS.items()
            if c.complexity != TaskComplexity.NONE
        ],
        "nodes_deterministic": [
            name for name, c in NODE_CONFIGS.items()
            if c.complexity == TaskComplexity.NONE
        ],
    }
