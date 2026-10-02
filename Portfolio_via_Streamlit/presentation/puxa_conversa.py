"""Cartas de perguntas para puxar assunto.

- Sem ``st.set_page_config`` (centralizado em ``app.py``).
- Chaves de ``session_state`` prefixadas com ``puxa_conversa_``.
- Leitura de arquivos cacheada com ``st.cache_data``.
- Navegacao via ``on_click``/``on_change`` para o card refletir o clique na hora.
"""

from __future__ import annotations

import random
from html import escape
from pathlib import Path

import streamlit as st

from Portfolio_via_Streamlit.config import QUESTIONS_DIR, WEB_ELEMENTS_DIR
from Portfolio_via_Streamlit.observability import safe_page, track_event

_PREFIX = "puxa_conversa_"
_KEY_INDEX = f"{_PREFIX}current_index"
_KEY_CATEGORIA = f"{_PREFIX}categoria"
_KEY_SHUFFLED = f"{_PREFIX}perguntas_shuffled"

_CATEGORIAS = ("profundas", "normais")
_ARQUIVOS = {
    "profundas": "perguntas_profundas.txt",
    "normais": "perguntas_normais.txt",
}


def _limpar_linha(linha: str) -> str:
    """Remove virgula final e aspas externas, caso o .txt esteja em formato de lista."""
    texto = linha.strip().rstrip(",").strip()
    if len(texto) >= 2 and texto[0] == texto[-1] and texto[0] in {'"', "'"}:
        texto = texto[1:-1]
    return texto.strip()


@st.cache_data(show_spinner=False)
def _carregar_perguntas() -> dict[str, list[str]]:
    perguntas: dict[str, list[str]] = {categoria: [] for categoria in _CATEGORIAS}
    for categoria, filename in _ARQUIVOS.items():
        path = Path(QUESTIONS_DIR) / filename
        if not path.exists():
            continue
        linhas = (_limpar_linha(linha) for linha in path.read_text(encoding="utf-8").splitlines())
        perguntas[categoria] = [linha for linha in linhas if linha and linha not in {"[", "]"}]
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
    # A pergunta e substituida por ultimo e escapada: evita que '<' ou '&' quebrem
    # o HTML e que um placeholder literal dentro da pergunta seja reprocessado.
    card_html = (
        template.replace("{{INDICE}}", str(indice))
        .replace("{{TOTAL}}", str(total))
        .replace("{{PERGUNTA}}", escape(pergunta))
    )
    st.markdown(card_html, unsafe_allow_html=True)


# --- Callbacks: rodam ANTES do rerun, entao o card ja sai atualizado ---


def _ao_trocar_categoria() -> None:
    st.session_state[_KEY_INDEX] = 0


def _ir_para_anterior() -> None:
    st.session_state[_KEY_INDEX] = max(0, st.session_state[_KEY_INDEX] - 1)


def _ir_para_proxima(total: int) -> None:
    st.session_state[_KEY_INDEX] = min(max(total - 1, 0), st.session_state[_KEY_INDEX] + 1)


def _resetar(categoria: str, perguntas: list[str]) -> None:
    st.session_state[_KEY_INDEX] = 0
    st.session_state[_KEY_SHUFFLED][categoria] = _embaralhar(perguntas)
    track_event("puxa_conversa_reset", categoria=categoria)


@safe_page("puxa_conversa")
def puxa_conversa_app() -> None:
    col_titulo, _ = st.columns([1, 2])
    with col_titulo:
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

    st.session_state.setdefault(_KEY_INDEX, 0)
    st.session_state.setdefault(_KEY_CATEGORIA, "normais")
    st.session_state.setdefault(_KEY_SHUFFLED, {})

    css = _carregar_css()
    if css:
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

    perguntas = _carregar_perguntas()
    if not st.session_state[_KEY_SHUFFLED]:
        st.session_state[_KEY_SHUFFLED] = {
            categoria: _embaralhar(lista) for categoria, lista in perguntas.items()
        }

    categoria = st.radio(
        "Escolha a categoria:",
        list(_CATEGORIAS),
        key=_KEY_CATEGORIA,
        on_change=_ao_trocar_categoria,
    )

    perguntas_atual = st.session_state[_KEY_SHUFFLED].get(categoria, [])
    total = len(perguntas_atual)

    idx = st.session_state[_KEY_INDEX]
    idx = max(0, min(idx, total - 1)) if total else 0
    st.session_state[_KEY_INDEX] = idx

    if total > 0:
        _renderizar_card(perguntas_atual[idx], idx + 1, total)
    else:
        st.write("Nenhuma pergunta encontrada nesta categoria.")

    col_anterior, col_reset, col_proxima = st.columns(3)
    with col_anterior:
        st.button(
            "⬅️ Anterior",
            on_click=_ir_para_anterior,
            disabled=idx <= 0,
            use_container_width=True,
        )
    with col_reset:
        st.button(
            "🔄 Reset",
            on_click=_resetar,
            args=(categoria, perguntas.get(categoria, [])),
            use_container_width=True,
        )
    with col_proxima:
        st.button(
            "➡️ Proxima",
            on_click=_ir_para_proxima,
            args=(total,),
            disabled=idx >= total - 1,
            use_container_width=True,
        )