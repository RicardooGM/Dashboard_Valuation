import streamlit as st

with open(".streamlit/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

with st.container(border=True):
    st.title("Taxa de Desconto")
    st.write("Página do Calculo da Taxa de Desconto")