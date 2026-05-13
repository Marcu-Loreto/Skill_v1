---
name: html-to-pptx
description: Converte apresentações HTML em arquivos .pptx editáveis compatíveis com PowerPoint e Google Apresentações. O conteúdo é exportado como texto editável (não como imagem), preservando títulos, bullets, imagens e estrutura de slides. Use esta skill sempre que o usuário pedir para converter HTML em PowerPoint, exportar apresentação como .pptx, gerar slides editáveis, transformar HTML em apresentação do Google Slides, ou mencionar termos como "converter para pptx", "exportar slides", "quero editar no PowerPoint", "abrir no Google Apresentações".
---

# HTML to PPTX — Conversor de Apresentações

## Objetivo

Converter arquivos HTML de apresentação em arquivos `.pptx` editáveis, compatíveis com Microsoft PowerPoint e Google Apresentações. Todo conteúdo deve ser texto editável — nunca renderizar slides como imagens.

## Dependência

Esta skill usa a biblioteca `python-pptx`. Antes de executar, verifique se está instalada:

```bash
pip install python-pptx beautifulsoup4 lxml requests
```

## Fluxo de Conversão

```
HTML Input → Parse (BeautifulSoup) → Extração de Slides → Mapeamento de Elementos → Geração PPTX → Arquivo Final
```

## Estratégia de Parsing

O conversor identifica slides no HTML por uma dessas estratégias (em ordem de prioridade):

1. Elementos com classe `.slide` ou `[id^="slide-"]`
2. Separadores `<hr>` ou `---` em Markdown convertido
3. Elementos `<section>` de nível superior

Para cada slide identificado, extrair:

### Elementos suportados

| HTML                    | PPTX equivalente                      |
| ----------------------- | ------------------------------------- |
| `<h1>`, `<h2>`          | Título do slide (title placeholder)   |
| `<h3>`                  | Subtítulo                             |
| `<p>`                   | Parágrafo no corpo do slide           |
| `<ul>`, `<ol>` + `<li>` | Lista com bullets/números             |
| `<img src="...">`       | Imagem inserida (download da URL)     |
| `<table>`               | Tabela nativa do PPTX                 |
| `<strong>`, `<b>`       | Texto em negrito                      |
| `<em>`, `<i>`           | Texto em itálico                      |
| `<span>` com cor inline | Texto colorido (extrair cor do style) |
| `.card`, `.stat`        | Caixa de texto com fundo              |

## Script de Conversão

Gere e execute um script Python que siga esta estrutura:

```python
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from bs4 import BeautifulSoup
import re
import requests
from io import BytesIO
from pathlib import Path


def parse_html_slides(html_path: str) -> list[dict]:
    """
    Lê o HTML e retorna uma lista de dicts, cada um representando um slide:
    {
        "title": str | None,
        "subtitle": str | None,
        "content": [
            {"type": "paragraph", "text": str, "bold": bool, "color": str|None},
            {"type": "bullet_list", "items": [str, ...]},
            {"type": "numbered_list", "items": [str, ...]},
            {"type": "image", "src": str, "alt": str},
            {"type": "table", "headers": [str], "rows": [[str]]},
        ]
    }
    """
    with open(html_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "lxml")

    slides_data = []
    slide_elements = soup.select(".slide, [id^='slide-']")

    if not slide_elements:
        slide_elements = soup.select("section")

    for slide_el in slide_elements:
        slide = {"title": None, "subtitle": None, "content": []}

        # Título
        title_el = slide_el.find(["h1", "h2"])
        if title_el:
            slide["title"] = title_el.get_text(strip=True)

        # Subtítulo
        subtitle_el = slide_el.find("h3")
        if subtitle_el:
            slide["subtitle"] = subtitle_el.get_text(strip=True)

        # Conteúdo
        for el in slide_el.find_all(["p", "ul", "ol", "img", "table", "div"], recursive=True):
            if el.name == "p" and el.parent == slide_el or el.find_parent(class_="card"):
                text = el.get_text(strip=True)
                if text and text != slide.get("title") and text != slide.get("subtitle"):
                    slide["content"].append({
                        "type": "paragraph",
                        "text": text,
                        "bold": bool(el.find(["strong", "b"])),
                        "color": None
                    })

            elif el.name in ("ul", "ol"):
                items = [li.get_text(strip=True) for li in el.find_all("li")]
                if items:
                    list_type = "bullet_list" if el.name == "ul" else "numbered_list"
                    slide["content"].append({"type": list_type, "items": items})

            elif el.name == "img":
                src = el.get("src", "")
                alt = el.get("alt", "")
                if src:
                    slide["content"].append({"type": "image", "src": src, "alt": alt})

            elif el.name == "table":
                headers = [th.get_text(strip=True) for th in el.find_all("th")]
                rows = []
                for tr in el.find_all("tr"):
                    cells = [td.get_text(strip=True) for td in tr.find_all("td")]
                    if cells:
                        rows.append(cells)
                if headers or rows:
                    slide["content"].append({"type": "table", "headers": headers, "rows": rows})

        slides_data.append(slide)

    return slides_data


def create_pptx(slides_data: list[dict], output_path: str, theme: str = "dark"):
    """
    Gera o arquivo .pptx a partir dos dados extraídos.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)  # Widescreen 16:9
    prs.slide_height = Inches(7.5)

    # Cores do tema
    if theme == "dark":
        bg_color = RGBColor(0x0F, 0x17, 0x2A)
        title_color = RGBColor(0xF1, 0xF5, 0xF9)
        text_color = RGBColor(0xCB, 0xD5, 0xE1)
        accent_color = RGBColor(0x22, 0xD3, 0xEE)
    else:
        bg_color = RGBColor(0xFF, 0xFF, 0xFF)
        title_color = RGBColor(0x1E, 0x29, 0x3B)
        text_color = RGBColor(0x33, 0x41, 0x55)
        accent_color = RGBColor(0x06, 0xB6, 0xD4)

    for slide_data in slides_data:
        # Usar layout em branco
        slide_layout = prs.slide_layouts[6]  # Blank
        slide = prs.slides.add_slide(slide_layout)

        # Background
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = bg_color

        y_position = Inches(0.5)

        # Título
        if slide_data["title"]:
            txBox = slide.shapes.add_textbox(Inches(0.8), y_position, Inches(11.5), Inches(1))
            tf = txBox.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.text = slide_data["title"]
            p.font.size = Pt(32)
            p.font.bold = True
            p.font.color.rgb = title_color
            y_position += Inches(1)

        # Subtítulo
        if slide_data["subtitle"]:
            txBox = slide.shapes.add_textbox(Inches(0.8), y_position, Inches(11.5), Inches(0.6))
            tf = txBox.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.text = slide_data["subtitle"]
            p.font.size = Pt(18)
            p.font.color.rgb = RGBColor(0x94, 0xA3, 0xB8)
            y_position += Inches(0.7)

        # Conteúdo
        for item in slide_data["content"]:
            if item["type"] == "paragraph":
                txBox = slide.shapes.add_textbox(
                    Inches(0.8), y_position, Inches(11.5), Inches(0.5)
                )
                tf = txBox.text_frame
                tf.word_wrap = True
                p = tf.paragraphs[0]
                p.text = item["text"]
                p.font.size = Pt(14)
                p.font.color.rgb = text_color
                if item.get("bold"):
                    p.font.bold = True
                y_position += Inches(0.5)

            elif item["type"] in ("bullet_list", "numbered_list"):
                txBox = slide.shapes.add_textbox(
                    Inches(0.8), y_position, Inches(11.5), Inches(len(item["items"]) * 0.4)
                )
                tf = txBox.text_frame
                tf.word_wrap = True
                for i, bullet in enumerate(item["items"]):
                    if i == 0:
                        p = tf.paragraphs[0]
                    else:
                        p = tf.add_paragraph()
                    prefix = f"{i+1}. " if item["type"] == "numbered_list" else "• "
                    p.text = prefix + bullet
                    p.font.size = Pt(13)
                    p.font.color.rgb = text_color
                    p.space_after = Pt(4)
                y_position += Inches(len(item["items"]) * 0.35 + 0.2)

            elif item["type"] == "image":
                src = item["src"]
                try:
                    if src.startswith("http"):
                        response = requests.get(src, timeout=10)
                        image_stream = BytesIO(response.content)
                        slide.shapes.add_picture(
                            image_stream, Inches(0.8), y_position, Inches(5), Inches(3)
                        )
                        y_position += Inches(3.2)
                except Exception:
                    # Se falhar, adicionar placeholder de texto
                    txBox = slide.shapes.add_textbox(
                        Inches(0.8), y_position, Inches(5), Inches(0.4)
                    )
                    tf = txBox.text_frame
                    p = tf.paragraphs[0]
                    p.text = f"[Imagem: {item.get('alt', src)}]"
                    p.font.size = Pt(11)
                    p.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)
                    y_position += Inches(0.5)

            elif item["type"] == "table":
                headers = item["headers"]
                rows = item["rows"]
                cols = max(len(headers), max((len(r) for r in rows), default=0))
                row_count = len(rows) + (1 if headers else 0)

                if cols > 0 and row_count > 0:
                    table_shape = slide.shapes.add_table(
                        row_count, cols,
                        Inches(0.8), y_position,
                        Inches(11.5), Inches(row_count * 0.45)
                    )
                    table = table_shape.table

                    # Headers
                    if headers:
                        for i, h in enumerate(headers):
                            if i < cols:
                                cell = table.cell(0, i)
                                cell.text = h

                    # Rows
                    offset = 1 if headers else 0
                    for r_idx, row in enumerate(rows):
                        for c_idx, cell_text in enumerate(row):
                            if c_idx < cols:
                                cell = table.cell(r_idx + offset, c_idx)
                                cell.text = cell_text

                    y_position += Inches(row_count * 0.45 + 0.3)

    prs.save(output_path)
    return output_path


def convert(html_path: str, output_path: str = None, theme: str = "dark") -> str:
    """Função principal de conversão."""
    if output_path is None:
        output_path = str(Path(html_path).with_suffix(".pptx"))

    slides_data = parse_html_slides(html_path)
    create_pptx(slides_data, output_path, theme=theme)
    return output_path


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Uso: python convert.py <arquivo.html> [arquivo_saida.pptx] [tema: dark|light]")
        sys.exit(1)

    html_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    theme = sys.argv[3] if len(sys.argv) > 3 else "dark"

    result = convert(html_file, output_file, theme)
    print(f"✅ Arquivo gerado: {result}")
```

## Como Usar

### Conversão direta

```bash
python .agent/skills/html-to-pptx/scripts/convert.py exports/minha-apresentacao.html
```

Isso gera `exports/minha-apresentacao.pptx` no mesmo diretório.

### Com tema claro (para fundos brancos)

```bash
python .agent/skills/html-to-pptx/scripts/convert.py exports/apresentacao.html exports/apresentacao.pptx light
```

### Imagens

O conversor detecta e baixa imagens que já existam no HTML:

- Tags `<img src="url">` (URLs externas são baixadas automaticamente)
- `background-image: url(...)` em style inline
- Atributos `data-src`

Para que o PPTX tenha imagens relevantes, inclua tags `<img>` no HTML de origem com URLs reais (Unsplash, Pexels, etc.) durante a geração da apresentação.

## Regras de Conversão

### O que DEVE ser texto editável (nunca imagem):

- Títulos (h1, h2, h3)
- Parágrafos
- Listas (bullets e numeradas)
- Tabelas
- Cards com texto

### O que pode ser imagem:

- Elementos `<img>` com src (baixar e inserir)
- Ícones/emojis (manter como texto Unicode)

### Preservação de formatação:

- Negrito → `font.bold = True`
- Itálico → `font.italic = True`
- Cores de texto → `font.color.rgb` (extrair do CSS inline)
- Tamanho de fonte → proporcional ao nível (h1 > h2 > p)

## Compatibilidade

O arquivo `.pptx` gerado é compatível com:

- Microsoft PowerPoint 2016+
- Google Apresentações (importar via Google Drive)
- LibreOffice Impress
- Apple Keynote (com importação)

Todos os elementos são editáveis — o usuário pode alterar textos, mover caixas, trocar imagens e reformatar livremente.

## Limitações Conhecidas

- CSS complexo (gradientes, sombras, border-radius) não é replicado no PPTX
- Layouts grid do HTML são convertidos em posicionamento sequencial vertical
- Animações e transições CSS são ignoradas
- Fontes customizadas podem não estar disponíveis no destino (usa fallback do sistema)

## Dicas

- Para melhor resultado visual, ajuste o layout manualmente no PowerPoint/Google após a conversão
- Use o tema `light` se a apresentação será projetada em ambientes claros
- Imagens com URLs externas precisam de conexão com internet durante a conversão
