"""
Presentation Generator — Chat Interface
Usuário digita o pedido, agente gera apresentação HTML completa.
"""

import streamlit as st
import re
from pathlib import Path
from datetime import date

from config import get_settings
from agents.research_node import research_node

settings = get_settings()

st.set_page_config(page_title="Gerador de Apresentações", page_icon="📊", layout="wide")
st.title("📊 Gerador de Apresentações")
st.markdown("Digite o que deseja e receba uma apresentação profissional.")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "generated_files" not in st.session_state:
    st.session_state.generated_files = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Ex: Crie uma apresentação sobre RAG avançado, 5 slides")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Gerando apresentação..."):
            try:
                from langchain_openai import ChatOpenAI
                from langchain_core.messages import SystemMessage, HumanMessage

                # Web search
                research_data = research_node({"tema": prompt, "publico": "Geral"}).get("research_results", [])
                research_context = ""
                if research_data:
                    research_context = "\n\nDADOS PESQUISADOS (use com citação):\n"
                    for i, r in enumerate(research_data[:6], 1):
                        research_context += f"[{i}] {r.get('title', '')} — {r.get('source', '')}\n"
                        research_context += f"    {r.get('snippet', '')[:200]}\n\n"

                system_msg = """Você é um gerador de apresentações profissionais em HTML.

REGRAS OBRIGATÓRIAS:
- HTML COMPLETO standalone com CSS embutido
- Dark theme (#0f172a bg, #f1f5f9 text)
- MÍNIMO 5 slides (a menos que o usuário peça menos)
- Use grids, cards (#1e293b), flow diagrams, code blocks
- Navegação por setas (← →) e botões
- Cada slide: div class="slide" id="slide-N", primeiro com class="slide active"
- Máximo 6 bullets por slide, 18 palavras por bullet
- Dados com fonte citada
- pt-BR
- Emojis em títulos de cards, cores: #06b6d4 accent, #34d399 highlight, #fbbf24 warn
- 16:9 (100vw x 100vh por slide)
- JavaScript para navegação
- GERE TODOS OS SLIDES — não pare no primeiro

FORMATO: Retorne APENAS HTML. Sem explicações. Sem markdown. Sem ```.
"""

                # LLM — fallback chain: MiniMax → OpenAI
                llm = None
                if settings.has_minimax:
                    try:
                        llm = ChatOpenAI(
                            model="MiniMax-M2.5",
                            api_key=settings.minimax_api_key,
                            base_url="https://api.minimaxi.chat/v1",
                            temperature=0.7,
                            max_tokens=32000,
                        )
                        llm.invoke([HumanMessage(content="ping")])
                    except Exception:
                        llm = None

                if not llm:
                    llm = ChatOpenAI(
                        model="gpt-4o-mini",
                        api_key=settings.openai_api_key,
                        temperature=0.7,
                        max_tokens=16000,
                    )

                response = llm.invoke([
                    SystemMessage(content=system_msg),
                    HumanMessage(content=prompt + research_context),
                ])

                html_content = response.content.strip()
                if html_content.startswith("```"):
                    html_content = re.sub(r"^```html?\n?", "", html_content)
                    html_content = re.sub(r"\n?```$", "", html_content)

                # Save
                exports_dir = Path("exports")
                exports_dir.mkdir(exist_ok=True)
                slug = re.sub(r"[\s]+", "-", re.sub(r"[^\w\s-]", "", prompt[:40].lower()))
                filename = f"{slug}-{date.today().isoformat()}.html"
                filepath = exports_dir / filename
                filepath.write_text(html_content, encoding="utf-8")

                st.session_state.generated_files.append(str(filepath))
                st.success(f"✅ Apresentação gerada: `{filepath}`")
                st.download_button("⬇️ Download HTML", html_content, filename, "text/html")
                st.session_state.messages.append({"role": "assistant", "content": f"✅ `{filepath}`"})

            except Exception as e:
                st.error(f"❌ Erro: {e}")
                st.session_state.messages.append({"role": "assistant", "content": f"❌ {e}"})

with st.sidebar:
    st.markdown("### 📁 Arquivos Gerados")
    for f in st.session_state.generated_files:
        st.markdown(f"- `{Path(f).name}`")
    if not st.session_state.generated_files:
        st.markdown("_Nenhum ainda._")
