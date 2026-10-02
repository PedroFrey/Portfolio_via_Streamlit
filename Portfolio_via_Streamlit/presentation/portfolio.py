"""Pagina de portfolio: apresentacao e projetos em destaque."""

from __future__ import annotations

import streamlit as st
from PIL import Image
from streamlit_lottie import st_lottie

from Portfolio_via_Streamlit.config import IMAGES_DIR
from Portfolio_via_Streamlit.logging_config import get_logger
from Portfolio_via_Streamlit.observability import safe_page, track_event
from Portfolio_via_Streamlit.services.lotties_service import load_lottie
from Portfolio_via_Streamlit.services.notifications_service import send_whatsapp_message

log = get_logger(__name__)

_NOTIFIED_KEY = "portfolio_notified"


def _notify_once_per_session() -> None:
    if st.session_state.get(_NOTIFIED_KEY):
        return
    st.session_state[_NOTIFIED_KEY] = True
    send_whatsapp_message("Alguem acessou o portfolio.")


def _load_image(filename: str) -> Image.Image | None:
    """Abre uma imagem de IMAGES_DIR. Retorna None se faltar ou estiver corrompida."""
    path = IMAGES_DIR / filename
    if not path.exists():
        log.warning("image_not_found", filename=filename)
        return None
    try:
        return Image.open(path)
    except Exception as exc:  # noqa: BLE001
        log.warning("image_load_failed", filename=filename, error=str(exc))
        return None


@safe_page("portfolio")
def portfolio_app() -> None:
    _notify_once_per_session()
    track_event("portfolio_page_viewed")

    img_financial = _load_image("cash-management-dashboard.png")
    img_pmo = _load_image("pmo.png")
    lottie_what_do_i_do = load_lottie("what_do_i_do.json")
    lottie_server = load_lottie("server.json")

    with st.container():
        st.subheader("Discover my Portfolio: P. Frey's Analytics Showcase")
        st.write(
            "Explore interactive data products, Streamlit web apps, and automated analytics solutions."
        )

    with st.container():
        st.write("---")
        left_col, right_col = st.columns(2)
        with left_col:
            st.header("What do I do")
            st.write("##")
            st.write(
                """
                Senior BI Developer & Analytics Engineer focused on data modeling, automation, and scalable platforms.
                Here you can find interactive web apps and data products built with Python (Streamlit)
                designed for scenario simulation, decision automation, and operational efficiency.
                """
            )
            st.write("[View my GitHub profile](https://github.com/PedroFrey)")
        with right_col:
            if lottie_what_do_i_do:
                st_lottie(lottie_what_do_i_do, key="lottie_what_do_i_do")
            st.write(":computer:")

    with st.container():
        st.write("---")
        image_col, text_col = st.columns((1, 2))
        with image_col:
            if img_financial:
                st.image(img_financial)
        with text_col:
            st.subheader("Data Visualization for Financial Analysis")
            st.write(
                "Financial Insights Dashboard: Comprehensive analysis of Cash Management and Corporate Metrics."
            )
            st.markdown("[Explore Financial Dashboard](https://www.google.com)")

    with st.container():
        st.write("---")
        image_col, text_col = st.columns((1, 2))
        with image_col:
            if img_pmo:
                st.image(img_pmo)
        with text_col:
            st.subheader("Project Management Dashboard")
            st.write("Real-time insights for Project, Program, and Portfolio performance.")
            st.markdown(
                "[Explore PMO Dashboard]"
                "(https://app.powerbi.com/view?r=eyJrIjoiYWMyZTIxOTItNzk2Ni00N2Q3LWE4YmUtNGViMWE0NjE3NzFlIiwidCI6ImUyZjc3ZDAwLTAxNjMtNGNmNi05MmIwLTQ4NGJhZmY5ZGY3ZCJ9)"
            )

    with st.container():
        st.write("---")
        if lottie_server:
            st_lottie(lottie_server, height=300, key="lottie_server")
        st.write("##")
        st.write(
            """
            To get in touch or discuss potential projects, feel free to reach out.
            I am open to collaborations and opportunities in Business Intelligence,
            Analytics Engineering, and Data Automation.
            """
        )
