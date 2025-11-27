import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.graph_objects as go

st.set_page_config(layout="wide")

# --- ESTILO PERSONALIZADO ---

# Carregar CSS externo
with open(".streamlit/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

#st.markdown(page_bg_img, unsafe_allow_html=True)


with st.container(border = True):
    st.title("Valuation de Empresas")
    st.write("Ferramenta de Valuation em página única. Insira os dados, analise e gere um relatório executivo.")

    with st.container(border = True):
        st.write("Ricardo de Oliveira Guimarães")



with st.container(border = True):
    
    st.subheader("DRE")

    # -------- PRIMEIRA LINHA --------
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        receita = st.number_input("**Receita líquida**",step=500000.0,format="%.2f")

    with col2:
        custos = st.number_input("**Custos**",step=500000.0,format="%.2f")

    with col3:
        despesas = st.number_input("**Despesas**",step=500000.0,format="%.2f") 

    with col4:

        ebitda = st.number_input("**EBITDA**",step=500000.0, format="%.2f")

    with col5:
        imposto = st.number_input("**Imposto**",step = 500000.0, format="%.2f")

    with col6:
        lucro_liq = st.number_input("**Lucro líquido**",step=500000.0, format="%.2f")

# -------- SEGUNDA LINHA --------

    st.subheader("Balanço Patrimonial")

    col6, col7, col8, col9 = st.columns(4)

    with col6:
        ativo = st.number_input("**Ativo**", step=500000.0,format="%.2f")

    with col7:
        passivo = st.number_input("**Passivo**",step=500000.0, format="%.2f")    

    with col8:
        divida_bruta = st.number_input("**Dívida bruta**",step=500000.0, format="%.2f")

    with col9:
        patrimonio_liq = st.number_input("**Patrimônio Líquido**",step=500000.0, format="%.2f")

    st.subheader("Fluxo de Caixa")
    # -------- TERCEIRA LINHA --------

    col10, col11, col12, col13=st.columns(4)        

    with col10:
        caixa = st.number_input("**Caixa e equivalentes**", step=500000.0, format="%.2f")

    with col11:
        capex = st.number_input("**CAPEX**",step=500000.0, format="%.2f")

    with col12:
        depreciacao = st.number_input("**Depreciação**",step=500000.0, format="%.2f")

    with col13:
        var_capital_de_giro = st.number_input("**Δ Capital de giro**", step=500000.0, format="%.2f")
        st.caption("Aumento consome caixa")

    lucro_bruto = receita - custos

     # -------- QUARTA LINHA --------

with st.container(border = True):

    st.subheader("Tabelas e Gráficos")

    col14, col15 = st.columns(2,vertical_alignment = "center")
    
    with col14:

        lucro_bruto = receita + custos

        df_dre = pd.DataFrame({
        "Item": ["Receita líquida","(-) Custos", "(=) Lucro Bruto","(-) Despesas","(=) EBITDA", "(-) Impostos","Lucro Líquido"],
        "Valor (R$)": [receita,custos,lucro_bruto,despesas,ebitda,imposto,lucro_liq]})

        df_dre["Variação da R.L %"] = [
        100 if receita != 0 else 0,
        (custos / receita) * 100 if receita != 0 else 0,
        (lucro_bruto / receita) * 100 if receita != 0 else 0,
        (despesas / receita) * 100 if receita != 0 else 0,
        (ebitda / receita) * 100 if receita != 0 else 0,
        (imposto / receita) * 100 if receita != 0 else 0,
        (lucro_liq / receita) * 100 if receita != 0 else 0
    ]
        st.table(df_dre)

    with col15:

        # Ordem visual da DRE
        # Ordem correta
        ordem = [
            "Receita líquida",
            "(-) Custos",
            "(=) Lucro Bruto",
            "(-) Despesas",
            "(=) EBITDA",
            "(-) Impostos",
            "Lucro Líquido"
        ]

        df_dre = df_dre.set_index("Item").loc[ordem].reset_index()

        items = df_dre["Item"].tolist()
        valores_plot = []

        # Tratamento correto dos valores para cascata
        for item, valor in zip(df_dre["Item"], df_dre["Valor (R$)"]):
            if item in ["(-) Custos", "(-) Despesas","(-) Impostos"]:
                valores_plot.append(-abs(valor))  # sempre descendente
            else:
                valores_plot.append(valor)        # totais mostram o valor real

        # Medidas no padrão Excel
        measure = [
            "relative",  # Receita líquida
            "relative",  # Custos
            "total",     # Lucro Bruto
            "relative",  # Despesas
            "total",     # EBITDA
            "relative",  # Impostos
            "total"      # Lucro Líquido
        ]

        fig = go.Figure(go.Waterfall(
            name="DRE",
            orientation="v",
            measure=measure,
            x=items,
            y=valores_plot,
            text=[f"R$ {abs(v):,.2f}" for v in valores_plot],
            textposition="outside",
            connector={"line": {"color": "rgb(120,120,120)"}},

            increasing={"marker": {"color": "#2ECC71"}},  # verde
            decreasing={"marker": {"color": "#E74C3C"}},  # vermelho
            totals={"marker": {"color": "#3498DB"}}       # azul
        ))

        fig.update_layout(
            title="DRE",
            showlegend=False,
            plot_bgcolor="#0F172A",
            paper_bgcolor="#0F172A",
            font=dict(color="#F1F5F9", family="Poppins"),
            xaxis=dict(tickangle=-15)
        )

        st.plotly_chart(fig, use_container_width=True)


# -------- QUINTA LINHA --------

    col16, col17 = st.columns(2,vertical_alignment = "center")

    with col16:
        
        fluxo_caixa_firma = lucro_liq + depreciacao - capex - var_capital_de_giro
        fluxo_caixa_acionista = fluxo_caixa_firma - divida_bruta

        fccaixa = pd.DataFrame({
        "Item2": ["Lucro Líquido","(+) Depreciação", "(-) CAPEX","(-) Δ Capital de Giro ","(=) Fluxo de Caixa da Firma","Fluxo de Caixa do Acionista"],
        "Valor2 (R$)": [lucro_liq,depreciacao,capex,var_capital_de_giro,fluxo_caixa_firma,fluxo_caixa_acionista]})

        st.table(fccaixa)

    with col17:

        df_ffcaixa_grafico = fccaixa.set_index("Item2")[["Valor2 (R$)"]]
        st.bar_chart(df_ffcaixa_grafico,sort = False)


# -------- SEXTA LINHA --------        

    col18, col19 = st.columns(2,vertical_alignment = "center")

    with col18:

        passivo_total = passivo + patrimonio_liq

        balanco = pd.DataFrame({
        "Descrição": ["Ativo","Passivo Total"],
        "3 - Valor (R$)": [ativo,passivo_total]})

        st.dataframe(balanco, use_container_width=True)

    with col19:

        df_balanco_grafico = balanco.set_index("Descrição")[["3 - Valor (R$)"]]
        st.bar_chart(df_balanco_grafico,sort = False)

    
with st.container(border = True):

    st.subheader("Indicadores")

    #primeira linha

    col20, col21 = st.columns(2)

    with col20:

        with st.container(border = True):

            st.write("Rentabilidade",unsafe_allow_html=False)

            col22, col23 = st.columns(2)

            with col22: 
                nopat = ebitda - depreciacao - imposto
                roic = nopat/(divida_bruta + patrimonio_liq)
                st.metric("ROIC",value = f"{roic*100:.2f}%", delta="20%",)

            with col22:
                roa = lucro_liq/ativo
                st.metric("ROA",value = f"{roa*100:.2f}%", delta="20%",)
                
            with col23:
                roe = lucro_liq/patrimonio_liq
                st.metric("ROE",value = f"{roe*100:.2f}%", delta="20%",)


    with col21:

        with st.container(border = True):

            st.write("Endividamento",unsafe_allow_html=False)

            col1, col2 = st.columns(2)

            with col1: 
                nopat = ebitda - depreciacao - imposto
                D_E = divida_bruta/patrimonio_liq
                st.metric("Debt/Equity",value = f"{D_E*100:.2f}%", delta="20%",)

            with col2:
                roe = divida_bruta/ebitda
                st.metric("Dívida/EBITDA",value = f"{roe*100:.2f}%", delta="20%",)

            with col1:
                roa = lucro_liq/ativo
                st.metric("ROA",value = f"{roa*100:.2f}%", delta="20%",)

    with col20:

         with st.container(border = True):

            st.write("Margens",unsafe_allow_html=False)

            col22, col23 = st.columns(2)

            with col22: 
                margem_bruta = lucro_bruto/receita
                st.metric("Margem Bruta",value = f"{margem_bruta*100:.2f}%", delta="20%",)

            with col22:
                nopat_re = nopat/receita
                st.metric("NOPAT/RECEITA",value = f"{nopat_re*100:.2f}%", delta="20%",)
                
            with col23:
                margem_ebitda = ebitda/receita
                st.metric("Margem EBITDA",value = f"{margem_ebitda*100:.2f}%", delta="20%",)
            
            with col23:
                margem_liq = lucro_liq/receita
                st.metric("Margem Líquida",value = f"{margem_liq*100:.2f}%", delta="20%",)

    with col21:

        with st.container(border = True):

            st.write("Endividamento",unsafe_allow_html=False)

            col1, col2 = st.columns(2)

            with col1: 
                nopat = ebitda - depreciacao + imposto
                D_E = divida_bruta/patrimonio_liq
                st.metric("Debt/Equity",value = f"{D_E*100:.2f}%", delta="20%",)

            with col2:
                roe = divida_bruta/ebitda
                st.metric("Dívida/EBITDA",value = f"{roe*100:.2f}%", delta="20%",)

            with col1:
                roa = lucro_liq/ativo
                st.metric("ROA",value = f"{roa*100:.2f}%", delta="20%",)

    






        

#container de indicadores
#container de wacc/capm
#container de multiplos
#container de Fleuriet
#Container de mensagem automatica
    


    

        
   



     



    