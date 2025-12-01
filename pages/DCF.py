import streamlit as st

with open(".streamlit/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

with st.container(border=True):
    st.title("Valuation DCF")
    st.write("Página de fluxo de caixa descontado")


