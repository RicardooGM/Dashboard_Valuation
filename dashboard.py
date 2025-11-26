import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.set_page_config(layout="wide")

with st.container(border = True):
    st.title("Valuation de Empresas")
    st.write("Ferramenta de valuation em página única. Insira dados, valide com IA e gere um relatório executivo em português.")



with st.container(border = True):
    
    st.subheader("DRE")

    # -------- PRIMEIRA LINHA --------
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        receita = st.number_input("**Receita líquida (12m)**",step=1000000.0,format="%.2f")

    with col2:
        custos = st.number_input("**Custos**",step=1000000.0,format="%.2f")

    with col3:
        despesas = st.number_input("**Despesas**",step=1000000.0,format="%.2f") 

    with col4:

        ebitda = st.number_input("**EBITDA (12m)**",step=1000000.0, format="%.2f")

    with col5:
        lucro_liq = st.number_input("**Lucro líquido (12m)**",step=1000000.0, format="%.2f")

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
        capex = st.number_input("**CAPEX (12m)**",step=1000000.0, format="%.2f")

    with col12:
        depreciacao = st.number_input("**Depreciação (12m)**",step=1000000.0, format="%.2f")

    with col13:
        var_capital_de_giro = st.number_input("**Δ Capital de giro (12m)**", step=1000000.0, format="%.2f")
        st.caption("Aumento consome caixa")

    lucro_bruto = receita - custos

     # -------- QUARTA LINHA --------

    st.subheader("Tabelas")

    col14, col15 = st.columns(2)
    
    with col14:

        lucro_bruto = receita - custos

        df_dre = pd.DataFrame({
        "Item": ["1 - Receita líquida","2 - Custos", "3 - Lucro Bruto","4 - Despesas","5 - EBITDA", "6 - Lucro Líquido"],
        "Valor (R$)": [receita,custos,lucro_bruto,despesas,ebitda,lucro_liq]})

        df_dre["Variação da R.L %"] = [
        100 if receita != 0 else 0,
        (custos / receita) * 100 if receita != 0 else 0,
        (lucro_bruto / receita) * 100 if receita != 0 else 0,
        (despesas / receita) * 100 if receita != 0 else 0,
        (ebitda / receita) * 100 if receita != 0 else 0,
        (lucro_liq / receita) * 100 if receita != 0 else 0
    ]

    with col15:

        fluxo_caixa_firma = lucro_liq + depreciacao - capex - var_capital_de_giro
        fluxo_caixa_acionista = fluxo_caixa_firma - divida_bruta

        fccaixa = pd.DataFrame({
        "Item2": ["1 - Lucro Líquido","2 - Depreciação", "3 - CAPEX","4 - Δ Capital de Giro ","5 - Fluxo de Caixa da Firma","6 - Fluxo de Caixa do Acionista"],
        "Valor2 (R$)": [lucro_liq,depreciacao,capex,var_capital_de_giro,fluxo_caixa_firma,fluxo_caixa_acionista]})

# -------- QUINTA LINHA --------

    col16,col17 = st.columns(2)

    with col16:

        st.dataframe(df_dre, use_container_width=True)

        df_dre_grafico = df_dre.set_index("Item")[["Valor (R$)"]]

        st.bar_chart(df_dre_grafico)

    with col17:

        st.dataframe(fccaixa, use_container_width=True)
        df_ffcaixa_grafico = fccaixa.set_index("Item2")[["Valor2 (R$)"]]
        st.bar_chart(df_ffcaixa_grafico)


    

        
   



     



    