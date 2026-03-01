# apps/portfolio.py
import streamlit as st
from PIL import Image
from streamlit_lottie import st_lottie
import os
from Portfolio_via_Streamlit.config import IMAGES_DIR
from Portfolio_via_Streamlit.services.lotties_service import load_lottie

# ------------------------
# Carregar imagens
# ------------------------
img_financial = Image.open(os.path.join(IMAGES_DIR, 'cash-management-dashboard.png'))
img_pmo = Image.open(os.path.join(IMAGES_DIR, 'pmo.png'))

# ------------------------
# Carregar Lotties do service
# ------------------------
lottie_what_do_i_do = load_lottie("what_do_i_do.json")
lottie_server = load_lottie("server.json")

# ------------------------
# Função principal do Portfolio App
# ------------------------
def portfolio_app():
    st.set_page_config(page_title="Portfolio P. Frey", layout="wide")

    # --- Header ---
    with st.container():
        st.subheader("Discover my Portfolio: P. Frey's Creative Showcase")
        st.write("Explore my work in data science with emphasis on data visualization!")

    # --- Apresentação ---
    with st.container():
        st.write("---")
        left_col, right_col = st.columns(2)
        with left_col:
            st.header("What do I do")
            st.write("##")
            st.write(
                """
                I am a data scientist specializing in data visualization.
                I transform complex data sets into meaningful insights through dashboards, charts, and interactive visuals.
                """
            )
            st.write("[View my GitHub profile](https://github.com/PedroFrey)")
        with right_col:
            if lottie_what_do_i_do:  # exibe somente se carregou
                st_lottie(lottie_what_do_i_do, key="lottie_what_do_i_do")
            st.write(":computer:")

    # --- Primeiro projeto ---
    with st.container():
        st.write("---")
        image_col, text_col = st.columns((1, 2))
        with image_col:
            st.image(img_financial)
        with text_col:
            st.subheader("Data Visualization for Financial Analysis")
            st.write("Financial Insights Dashboard: Comprehensive analysis of [Company/Market/Industry].")
            st.markdown("[Explore Financial Dashboard](https://www.google.com)")

    # --- Segundo projeto ---
    with st.container():
        st.write("---")
        image_col, text_col = st.columns((1, 2))
        with image_col:
            st.image(img_pmo)
        with text_col:
            st.subheader("Project Management Dashboard")
            st.write("Real-time insights for Project/Program/Portfolio performance.")
            st.markdown(
                "[Explore PMO Dashboard](https://app.powerbi.com/view?r=eyJrIjoiYWMyZTIxOTItNzk2Ni00N2Q3LWE4YmUtNGViMWE0NjE3NzFlIiwidCI6ImUyZjc3ZDAwLTAxNjMtNGNmNi05MmIwLTQ4NGJhZmY5ZGY3ZCJ9)"
            )

    # --- Fechamento ---
    with st.container():
        st.write("---")
        if lottie_server:
            st_lottie(lottie_server, height=300, key="lottie_server")
        st.write("##")
        st.write(
            """
            To get in touch or inquire about projects, feel free to send me an email.
            I am always open to collaborations and new opportunities in data science and visualization.
            """
        )