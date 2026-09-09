"""Cartas de perguntas para puxar assunto.

- Sem ``st.set_page_config`` (centralizado em ``app.py``).
- Chaves de ``session_state`` prefixadas com ``puxa_conversa_``.
- Leitura de arquivos cacheada com ``st.cache_data``.
"""

from __future__ import annotations

import random
from pathlib import Path

import streamlit as st

from Portfolio_via_Streamlit.config import QUESTIONS_DIR, WEB_ELEMENTS_DIR
from Portfolio_via_Streamlit.observability import safe_page, track_event

_PREFIX = "puxa_conversa_"


@st.cache_data(show_spinner=False)
def _carregar_perguntas() -> dict[str, list[str]]:
    perguntas: dict[str, list[str]] = {"profundas": [], "normais": []}
    for categoria, filename in (
        ("profundas", "perguntas_profundas.txt"),
        ("normais", "perguntas_normais.txt"),
    ):
        path = Path(QUESTIONS_DIR) / filename
        if path.exists():
            perguntas[categoria] = [
                linha.strip()
                for linha in path.read_text(encoding="utf-8").splitlines()
                if linha.strip()
            ]
    return perguntas


@st.cache_data(show_spinner=False)
def _carregar_css() -> str | None:
    path = Path(WEB_ELEMENTS_DIR) / "style.css"
    return path.read_text(encoding="utf-8") if path.exists() else None


@st.cache_data(show_spinner=False)
def _carregar_template_card() -> str | None:
    path = Path(WEB_ELEMENTS_DIR) / "card.html"
    return path.read_text(encoding="utf-8") if path.exists() else None


def _embaralhar(perguntas: list[str]) -> list[str]:
    copia = perguntas.copy()
    random.shuffle(copia)
    return copia


def _renderizar_card(pergunta: str, indice: int, total: int) -> None:
    template = _carregar_template_card()
    if template is None:
        st.write("Card HTML nao encontrado!")
        return
    html = (
        template.replace("{{PERGUNTA}}", pergunta)
        .replace("{{INDICE}}", str(indice))
        .replace("{{TOTAL}}", str(total))
    )
    st.markdown(html, unsafe_allow_html=True)


@safe_page("puxa_conversa")
def puxa_conversa_app() -> None:
    col1, _ = st.columns([1, 2])
    with col1:
        st.markdown(
            """
            <div style='padding: 1rem 0;'>
                <h1 style='font-size: 2rem; margin-bottom: 0.5rem;
                    background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
                💬 Puxa-Conversa
                </h1>
                <p style='color: #666; font-size: 0.9rem;'>Navegue pelas perguntas!</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    estado_padrao = {
        f"{_PREFIX}current_index": 0,
        f"{_PREFIX}categoria": "normais",
        f"{_PREFIX}perguntas_shuffled": {},
    }
    for chave, valor in estado_padrao.items():
        st.session_state.setdefault(chave, valor)

    css = _carregar_css()
    if css:
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

    perguntas = _carregar_perguntas()
    if not st.session_state[f"{_PREFIX}perguntas_shuffled"]:
        st.session_state[f"{_PREFIX}perguntas_shuffled"] = {
            cat: _embaralhar(lista) for cat, lista in perguntas.items()
        }

    categoria = st.radio(
        "Escolha a categoria:",
        ["profundas", "normais"],
        index=0 if st.session_state[f"{_PREFIX}categoria"] == "profundas" else 1,
    )
    if categoria != st.session_state[f"{_PREFIX}categoria"]:
        st.session_state[f"{_PREFIX}categoria"] = categoria
        st.session_state[f"{_PREFIX}current_index"] = 0

    perguntas_atual = st.session_state[f"{_PREFIX}perguntas_shuffled"][categoria]
    total = len(perguntas_atual)

    idx = st.session_state[f"{_PREFIX}current_index"]
    idx = max(0, min(idx, total - 1)) if total else 0
    st.session_state[f"{_PREFIX}current_index"] = idx

    if total > 0:
        _renderizar_card(perguntas_atual[idx], idx + 1, total)
    else:
        st.write("Nenhuma pergunta encontrada nesta categoria.")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("⬅️ Anterior") and idx > 0:
            st.session_state[f"{_PREFIX}current_index"] -= 1
    with col2:
        if st.button("🔄 Reset"):
            st.session_state[f"{_PREFIX}current_index"] = 0
            st.session_state[f"{_PREFIX}perguntas_shuffled"][categoria] = _embaralhar(
                perguntas[categoria]
            )
            track_event("puxa_conversa_reset", categoria=categoria)
    with col3:
        if st.button("➡️ Proxima") and idx < total - 1:
            st.session_state[f"{_PREFIX}current_index"] += 1
