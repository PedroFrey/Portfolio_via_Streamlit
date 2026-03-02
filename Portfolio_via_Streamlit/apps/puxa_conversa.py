import streamlit as st
import os
import random

# --- Caminhos ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
WEB_ELEMENTS_DIR = os.path.join(ASSETS_DIR, "WebDevElements")
QUESTIONS_DIR = os.path.join(ASSETS_DIR, "questions")

def Puxa_Conversa():
    # --- Configuração da página ---
    st.set_page_config(page_title="💬 Puxa-Conversa", page_icon="💡", layout="wide")

    # --- Session state ---
    if 'current_index' not in st.session_state:
        st.session_state.current_index = 0
    if 'categoria' not in st.session_state:
        st.session_state.categoria = 'normais'
    if 'perguntas' not in st.session_state:
        st.session_state.perguntas = {'profundas': [], 'normais': []}
    if 'perguntas_shuffled' not in st.session_state:
        st.session_state.perguntas_shuffled = {'profundas': [], 'normais': []}

    # --- Função: carregar perguntas ---
    def carregar_perguntas():
        prof_path = os.path.join(QUESTIONS_DIR, "perguntas_profundas.txt")
        norm_path = os.path.join(QUESTIONS_DIR, "perguntas_normais.txt")
        if os.path.exists(prof_path):
            with open(prof_path, "r", encoding="utf-8") as f:
                st.session_state.perguntas['profundas'] = [l.strip() for l in f if l.strip()]
        if os.path.exists(norm_path):
            with open(norm_path, "r", encoding="utf-8") as f:
                st.session_state.perguntas['normais'] = [l.strip() for l in f if l.strip()]

    # --- Função: embaralhar perguntas ---
    def shuffle_perguntas(categoria):
        perguntas = st.session_state.perguntas.get(categoria, []).copy()
        random.shuffle(perguntas)
        return perguntas

    # --- Função: carregar CSS ---
    def carregar_css():
        css_path = os.path.join(WEB_ELEMENTS_DIR, "style.css")
        if os.path.exists(css_path):
            with open(css_path, "r", encoding="utf-8") as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # --- Função: renderizar card HTML ---
    def renderizar_card_html(pergunta, indice, total):
        card_path = os.path.join(WEB_ELEMENTS_DIR, "card.html")
        if os.path.exists(card_path):
            with open(card_path, "r", encoding="utf-8") as f:
                html = f.read()
            html = html.replace("{{PERGUNTA}}", pergunta)
            html = html.replace("{{INDICE}}", str(indice))
            html = html.replace("{{TOTAL}}", str(total))
            st.markdown(html, unsafe_allow_html=True)
        else:
            st.write("Card HTML não encontrado!")

    # --- Carregar CSS apenas uma vez ---
    carregar_css()

    # --- Carregar perguntas se ainda não carregou ---
    if not st.session_state.perguntas['profundas']:
        carregar_perguntas()
        for cat in ['profundas', 'normais']:
            st.session_state.perguntas_shuffled[cat] = shuffle_perguntas(cat)

    # --- Seleção de categoria ---
    categoria = st.radio(
        "Escolha a categoria:", ['profundas', 'normais'],
        index=0 if st.session_state.categoria=='profundas' else 1
    )
    st.session_state.categoria = categoria

    perguntas_atual = st.session_state.perguntas_shuffled[categoria]
    total_perguntas = len(perguntas_atual)

    # --- Garantir índice válido ---
    if st.session_state.current_index >= total_perguntas:
        st.session_state.current_index = total_perguntas - 1
    if st.session_state.current_index < 0:
        st.session_state.current_index = 0

    # --- Renderizar pergunta atual ---
    if total_perguntas > 0:
        renderizar_card_html(
            perguntas_atual[st.session_state.current_index],
            st.session_state.current_index + 1,
            total_perguntas
        )
    else:
        st.write("Nenhuma pergunta encontrada nesta categoria.")

    # --- Navegação ---
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("⬅️ Anterior"):
            if st.session_state.current_index > 0:
                st.session_state.current_index -= 1
    with col2:
        if st.button("🔄 Reset"):
            st.session_state.current_index = 0
            st.session_state.perguntas_shuffled[categoria] = shuffle_perguntas(categoria)
    with col3:
        if st.button("➡️ Próxima"):
            if st.session_state.current_index < total_perguntas - 1:
                st.session_state.current_index += 1