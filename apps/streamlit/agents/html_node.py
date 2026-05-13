"""
HTML Generation Node - Produces standalone HTML presentation.
No LLM needed - deterministic template rendering.
"""

import re
import json
from pathlib import Path
from datetime import date


def get_theme_colors(template_name):
    """Load colors from template registry or use defaults."""
    try:
        from config import get_settings
        settings = get_settings()
        registry_path = settings.templates_dir / "registry.json"
        if registry_path.exists():
            with open(registry_path, "r", encoding="utf-8") as f:
                templates = json.load(f)
            for t in templates:
                if t["name"] == template_name:
                    return t["colors"]
    except Exception:
        pass
    return {
        "primary": "#22d3ee",
        "secondary": "#0f172a",
        "accent": "#818cf8",
        "background": "#0f172a",
        "text": "#f1f5f9",
    }


def escape_html(text):
    """Escape HTML special characters."""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def render_slide_html(slide, slide_num, total):
    """Render a single slide as HTML."""
    title = escape_html(slide.get("title", ""))
    subtitle = escape_html(slide.get("subtitle", ""))
    content = slide.get("content", [])
    is_active = " active" if slide_num == 1 else ""

    content_html = ""
    if content:
        content_html = "<ul>\n"
        for bullet in content:
            content_html += "            <li>" + escape_html(bullet) + "</li>\n"
        content_html += "          </ul>"

    subtitle_html = "        <h3>" + subtitle + "</h3>\n" if subtitle else ""

    html = '    <div class="slide' + is_active + '" id="slide-' + str(slide_num) + '">\n'
    html += "        <h2>" + title + "</h2>\n"
    html += subtitle_html
    html += '        <div class="slide-content">\n'
    html += "          " + content_html + "\n"
    html += "        </div>\n"
    html += '        <div class="slide-number">' + str(slide_num) + " / " + str(total) + "</div>\n"
    html += "    </div>\n"
    return html


def generate_html(slides, tema, template_name="Padrao (dark theme)"):
    """Generate complete standalone HTML presentation."""
    colors = get_theme_colors(template_name)
    total = len(slides)

    bg = colors.get("background", "#0f172a")
    text_color = colors.get("text", "#f1f5f9")
    primary = colors.get("primary", "#22d3ee")
    accent = colors.get("accent", "#818cf8")

    is_dark = bg.lower() in ("#0f172a", "#0a0e1a", "#1e293b", "#000000", "#111827")
    subtitle_color = "#94a3b8" if is_dark else "#64748b"
    nav_bg = "#1e293b" if is_dark else "#f1f5f9"
    nav_border = "#334155" if is_dark else "#e2e8f0"
    title_color = text_color if is_dark else primary
    slide_border = "border-top: 4px solid " + primary + ";" if not is_dark else ""

    slides_html = ""
    for i, slide in enumerate(slides, 1):
        slides_html += render_slide_html(slide, i, total)

    css = "* { margin: 0; padding: 0; box-sizing: border-box; }\n"
    css += "body { font-family: 'Segoe UI', system-ui, sans-serif; "
    css += "background: " + bg + "; color: " + text_color + "; overflow: hidden; height: 100vh; }\n"
    css += ".slide { display: none; width: 100vw; height: 100vh; padding: 60px 80px; "
    css += "position: relative; flex-direction: column; justify-content: center; " + slide_border + " }\n"
    css += ".slide.active { display: flex; }\n"
    css += ".slide-number { position: absolute; bottom: 30px; right: 40px; font-size: 14px; color: " + subtitle_color + "; }\n"
    css += ".nav { position: fixed; bottom: 30px; left: 50%; transform: translateX(-50%); display: flex; gap: 12px; z-index: 100; }\n"
    css += ".nav button { background: " + nav_bg + "; border: 1px solid " + nav_border + "; "
    css += "color: " + text_color + "; padding: 10px 20px; border-radius: 8px; cursor: pointer; font-size: 14px; }\n"
    css += ".nav button:hover { border-color: " + primary + "; }\n"
    css += "h2 { font-size: 2.4rem; font-weight: 600; margin-bottom: 24px; color: " + title_color + "; }\n"
    css += "h3 { font-size: 1.3rem; font-weight: 400; color: " + subtitle_color + "; margin-bottom: 20px; }\n"
    css += ".slide-content { max-width: 900px; }\n"
    css += "ul { list-style: none; padding: 0; }\n"
    css += "ul li { font-size: 1.2rem; line-height: 1.9; color: " + text_color + "; "
    css += "padding-left: 28px; position: relative; margin-bottom: 8px; }\n"
    css += "ul li::before { content: '\\2192'; position: absolute; left: 0; color: " + primary + "; }\n"

    js = "let current = 1; const total = " + str(total) + ";\n"
    js += "function showSlide(n) { document.querySelectorAll('.slide').forEach(s => s.classList.remove('active')); "
    js += "document.getElementById('slide-' + n).classList.add('active'); current = n; }\n"
    js += "function nextSlide() { if (current < total) showSlide(current + 1); }\n"
    js += "function prevSlide() { if (current > 1) showSlide(current - 1); }\n"
    js += "document.addEventListener('keydown', (e) => { "
    js += "if (e.key === 'ArrowRight' || e.key === 'ArrowDown') nextSlide(); "
    js += "if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') prevSlide(); });\n"

    html = '<!DOCTYPE html>\n<html lang="pt-BR">\n<head>\n'
    html += '  <meta charset="UTF-8">\n'
    html += '  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
    html += "  <title>" + escape_html(tema) + "</title>\n"
    html += "  <style>" + css + "</style>\n"
    html += "</head>\n<body>\n"
    html += slides_html
    html += '  <div class="nav">\n'
    html += '    <button onclick="prevSlide()">&larr; Anterior</button>\n'
    html += '    <button onclick="nextSlide()">Pr&oacute;ximo &rarr;</button>\n'
    html += "  </div>\n"
    html += "  <script>" + js + "</script>\n"
    html += "</body>\n</html>"

    return html


def html_node(state):
    """
    LangGraph node: HTML Generation.
    Converts structured slides into standalone HTML.
    No LLM needed - deterministic rendering.
    """
    slides = state.get("slides", [])
    tema = state.get("tema", "Apresentacao")
    template = state.get("template", "Padrao (dark theme)")

    if not slides:
        result = dict(state)
        result["html_content"] = ""
        result["html_path"] = ""
        result["error"] = "Nenhum slide para renderizar"
        return result

    html_content = generate_html(slides, tema, template)

    try:
        from config import get_settings
        settings = get_settings()
        exports_dir = settings.exports_dir
    except Exception:
        exports_dir = Path("exports")

    exports_dir.mkdir(parents=True, exist_ok=True)

    slug = re.sub(r"[^\w\s-]", "", tema.lower())
    slug = re.sub(r"[\s]+", "-", slug)[:50]
    filename = slug + "-" + date.today().isoformat() + ".html"
    html_path = exports_dir / filename

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    result = dict(state)
    result["html_content"] = html_content
    result["html_path"] = str(html_path)
    return result
