import streamlit as st

def calculate_unit_price(price, quantity):
        return price / quantity if quantity != 0 else float('inf')

def price_comparator():

    st.set_page_config(page_title="Supermarket Price Comparator", page_icon="🛒", layout="centered")
    
    st.title("🛒 Supermarket Price Comparator")
    st.subheader("Quickly check which product is cheaper per unit!")
    
    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.header("🔍 Product 1")
        price1 = st.number_input("Price (R$)", min_value=0.0, value=10.0, step=0.01, key="price1")
        quantity1 = st.number_input("Quantity (kg, L, units...)", min_value=0.01, value=1.0, step=0.1, key="quantity1")
        
        st.markdown("---")
    with col2:
        st.header("🔍 Product 2")
        price2 = st.number_input("Price (R$)", min_value=0.0, value=8.0, step=0.01, key="price2")
        quantity2 = st.number_input("Quantity (kg, L, units...)", min_value=0.01, value=0.8, step=0.1, key="quantity2")
        
        st.markdown("---")
    
    if st.button("🚀 Compare Now"):
        unit_price1 = calculate_unit_price(price1, quantity1)
        unit_price2 = calculate_unit_price(price2, quantity2)
    
        st.subheader("💡 Result")
    
        st.write(f"🔸 Product 1 unit price: **R$ {unit_price1:.2f}**")
        st.write(f"🔸 Product 2 unit price: **R$ {unit_price2:.2f}**")
    
        if unit_price1 < unit_price2:
            st.success("✅ **Product 1 is more cost-effective!**")
        elif unit_price2 < unit_price1:
            st.success("✅ **Product 2 is more cost-effective!**")
        else:
            st.info("⚖️ **Both products have the same unit price.**")
    
    st.markdown("---")
    st.caption("Tip: Quantity can be in kg, liters, units, packs, etc.")