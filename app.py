import streamlit as st
from Portfolio_via_Streamlit.apps import portfolio, retirement , puxa_conversa,price_comparator #,stocks
from Portfolio_via_Streamlit.services.notifications_service import send_whatsapp_message

#==========
# Informações Gerais
# Para Rodar no Navegador: python -m streamlit run app.py
#==========

# Chama ao iniciar a app
if "notified" not in st.session_state:
    send_whatsapp_message("Entraram no Render")
    st.session_state.notified = True


page_names_to_funcs = {
    "My Portfolio": portfolio.portfolio_app,
    "Retirement App": retirement.retirement_app,
    "Puxa Conversa": puxa_conversa.Puxa_Conversa,
    "Price Comparator App": price_comparator.price_comparator,
#     "Stocks App": stocks.stock_dashboard,
}

st.set_page_config(
    page_title="P. Frey's Creative Showcase",
    page_icon=':computer:',
    layout='wide'
)

selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()
