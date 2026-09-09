"""Pagina inicial: catalogo dos mini-apps, com contexto antes de navegar."""

from __future__ import annotations

import streamlit as st

from Portfolio_via_Streamlit.observability import safe_page

_APPS = [
    ("🧑‍💻", "My Portfolio", "Quem sou eu e os projetos em destaque."),
    (
        "💰",
        "Retirement App",
        "Simulador de aposentadoria com aportes, eventos e projecao mes a mes.",
    ),
    ("🛒", "Price Comparator App", "Compara o preco por unidade entre dois produtos."),
    ("💬", "Puxa Conversa", "Cartas com perguntas para puxar assunto, estilo Tinder."),
]


@safe_page("home")
def home_app() -> None:
    st.title("👋 Bem-vindo ao meu Showcase")
    st.write(
        "Esse e um portfolio pessoal com alguns mini-apps de dados. "
        "Use o menu a esquerda para navegar entre eles."
    )
    st.markdown("---")

    for icon, nome, descricao in _APPS:
        col_icon, col_text = st.columns([1, 8])
        with col_icon:
            st.markdown(f"### {icon}")
        with col_text:
            st.markdown(f"**{nome}**")
            st.caption(descricao)
        st.markdown("")
