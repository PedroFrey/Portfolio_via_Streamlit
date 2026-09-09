"""Entry point. Rodar com: streamlit run app.py
 
Responsabilidades deste arquivo, e so dele:
- st.set_page_config (deve ser chamado uma unica vez, antes de qualquer
  outro comando Streamlit).
- Inicializacao de observabilidade (logging + Sentry) uma vez por processo.
- Definicao da navegacao nativa (st.navigation/st.Page).
"""

from __future__ import annotations

import streamlit as st

from Portfolio_via_Streamlit.logging_config import configure_logging
from Portfolio_via_Streamlit.observability import init_sentry

st.set_page_config(
    page_title="P. Frey's Creative Showcase",
    page_icon=":computer:",
    layout="wide",
)

configure_logging()
init_sentry()

from Portfolio_via_Streamlit.presentation.home import home_app  # noqa: E402
from Portfolio_via_Streamlit.presentation.portfolio import portfolio_app  # noqa: E402
from Portfolio_via_Streamlit.presentation.price_comparator import price_comparator  # noqa: E402
from Portfolio_via_Streamlit.presentation.puxa_conversa import puxa_conversa_app  # noqa: E402
from Portfolio_via_Streamlit.presentation.retirement import retirement_app  # noqa: E402

pages = [
    st.Page(home_app, title="Home", icon="🏠", default=True),
    st.Page(portfolio_app, title="My Portfolio", icon="🧑‍💻"),
    st.Page(retirement_app, title="Retirement App", icon="💰"),
    st.Page(price_comparator, title="Price Comparator App", icon="🛒"),
    st.Page(puxa_conversa_app, title="Puxa Conversa", icon="💬"),
]

navigation = st.navigation(pages)
navigation.run()
