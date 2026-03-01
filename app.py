import streamlit as st
from Portfolio_via_Streamlit.apps import portfolio#, retirement, stocks, price_comparator, puxa_conversa

page_names_to_funcs = {
    "My Portfolio": portfolio.portfolio_app,
#     "Retirement App": retirement.retirement_app,
#     "Stocks App": stocks.stock_dashboard,
#     "Price Comparator App": price_comparator.price_comparator,
#     "Puxa Conversa": puxa_conversa.Puxa_Conversa
}

st.set_page_config(
    page_title="P. Frey's Creative Showcase",
    page_icon=':computer:',
    layout='wide'
)

selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()