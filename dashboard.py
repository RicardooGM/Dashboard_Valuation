import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.set_page_config(layout="wide")

# --- ESTILO PERSONALIZADO ---
st.markdown("""
    <style>
        /* Importando a fonte Inter */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

        /* Aplicar fonte INTER para todo o app */
        html, body, div, span, p, input, textarea, button, label {
            font-family: 'Inter', sans-serif !important;
        }

        .stMarkdown, .stTextInput, .stSelectbox, .stRadio, .stCheckbox, .stButton>button {
            font-family: 'Inter', sans-serif !important;
        }

        /* Fundo principal */
        .stApp {
            background-color: #0F172A !important;
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: #1E293B !important;
        }

        /* Cor dos textos */
        h1, h2, h3, h4, h5, h6, p, label {
            color: #F1F5F9 !important;
        }

        /* 🔥 Ajuste de fonte dos números dos eixos st.bar_chart (Altair) */
        .vega-embed text {
            font-size: 10px !important;
            fill: #F1F5F9 !important; /* melhora visibilidade no modo escuro */
        }

    </style>
""", unsafe_allow_html=True)



#st.markdown(page_bg_img, unsafe_allow_html=True)


with st.container(border = True):
    st.title("Valuation de Empresas")
    st.write("Ferramenta de valuation em página única. Insira dados, valide com IA e gere um relatório executivo em português.")



with st.container(border = True):
    
    st.subheader("DRE")

    # -------- PRIMEIRA LINHA --------
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        receita = st.number_input("**Receita líquida**",step=1000000.0,format="%.2f")

    with col2:
        custos = st.number_input("**Custos**",step=1000000.0,format="%.2f")

    with col3:
        despesas = st.number_input("**Despesas**",step=1000000.0,format="%.2f") 

    with col4:

        ebitda = st.number_input("**EBITDA**",step=1000000.0, format="%.2f")

    with col5:
        lucro_liq = st.number_input("**Lucro líquido**",step=1000000.0, format="%.2f")

# -------- SEGUNDA LINHA --------

    st.subheader("Balanço Patrimonial")

    col6, col7, col8, col9 = st.columns(4)

    with col6:
        ativo = st.number_input("**Ativo**", step=1000000.0,format="%.2f")

    with col7:
        passivo = st.number_input("**Passivo**",step=1000000.0, format="%.2f")    

    with col8:
        divida_bruta = st.number_input("**Dívida bruta**",step=1000000.0, format="%.2f")

    with col9:
        patrimonio_liq = st.number_input("**Patrimônio Líquido**",step=1000000.0, format="%.2f")

    st.subheader("Fluxo de Caixa")
    # -------- TERCEIRA LINHA --------

    col10, col11, col12, col13=st.columns(4)        

    with col10:
        caixa = st.number_input("**Caixa e equivalentes**", step=1000000.0, format="%.2f")

    with col11:
        capex = st.number_input("**CAPEX**",step=1000000.0, format="%.2f")

    with col12:
        depreciacao = st.number_input("**Depreciação**",step=1000000.0, format="%.2f")

    with col13:
        var_capital_de_giro = st.number_input("**Δ Capital de giro**", step=1000000.0, format="%.2f")
        st.caption("Aumento consome caixa")

    lucro_bruto = receita - custos

     # -------- QUARTA LINHA --------

    st.subheader("Tabelas")

    col14, col15, col16 = st.columns(3)
    
    with col14:

        lucro_bruto = receita - custos

        df_dre = pd.DataFrame({
        "Item": ["Receita líquida","(-) Custos", "(=) Lucro Bruto","(-) Despesas","(=) EBITDA", "Lucro Líquido"],
        "Valor (R$)": [receita,custos,lucro_bruto,despesas,ebitda,lucro_liq]})

        df_dre["Variação da R.L %"] = [
        100 if receita != 0 else 0,
        (custos / receita) * 100 if receita != 0 else 0,
        (lucro_bruto / receita) * 100 if receita != 0 else 0,
        (despesas / receita) * 100 if receita != 0 else 0,
        (ebitda / receita) * 100 if receita != 0 else 0,
        (lucro_liq / receita) * 100 if receita != 0 else 0
    ]
        st.dataframe(df_dre, use_container_width=True)

    with col15:

        fluxo_caixa_firma = lucro_liq + depreciacao - capex - var_capital_de_giro
        fluxo_caixa_acionista = fluxo_caixa_firma - divida_bruta

        fccaixa = pd.DataFrame({
        "Item2": ["Lucro Líquido","(+) Depreciação", "(-) CAPEX","(+) Capital de Giro ","(=) Fluxo de Caixa da Firma","Fluxo de Caixa do Acionista"],
        "Valor2 (R$)": [lucro_liq,depreciacao,capex,var_capital_de_giro,fluxo_caixa_firma,fluxo_caixa_acionista]})

        st.dataframe(fccaixa, use_container_width=True)

    with col16:

        passivo_total = passivo + patrimonio_liq

        balanco = pd.DataFrame({
        "Descrição": ["Ativo","Passivo Total"],
        "3 - Valor (R$)": [ativo,passivo_total]})

        st.dataframe(balanco, use_container_width=True)
        

# -------- QUINTA LINHA --------

    st.subheader("Gráficos")

    col17,col18,col19 = st.columns(3)

    with col17:

        df_dre_grafico = df_dre.set_index("Item")[["Valor (R$)"]]
        st.bar_chart(df_dre_grafico,sort = False)

    with col18:

        df_ffcaixa_grafico = fccaixa.set_index("Item2")[["Valor2 (R$)"]]
        st.bar_chart(df_ffcaixa_grafico,sort = False)

    with col19:

        df_balanco_grafico = balanco.set_index("Descrição")[["3 - Valor (R$)"]]
        st.bar_chart(df_balanco_grafico,sort = False)

    


    

        
   



     



    