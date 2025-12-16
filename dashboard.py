import os
import requests
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf
import numpy as np
import plotly.graph_objects as go
from setores import SETORES_EMPRESAS
import plotly.express as px


load_dotenv()
FRED_API_KEY = os.getenv("FRED_API_KEY")


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
        "Item": ["Receita líquida","(-) Custos", "(=) Lucro Bruto","(-) Despesas","(=) EBITDA", "(-) Impostos","(=) Lucro Líquido"],
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
            "(=) Lucro Líquido"
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
        "Item2": ["Lucro Líquido","(+) Depreciação", "(-) CAPEX","(-) Δ Capital de Giro","(=) Fluxo de Caixa da Firma","Fluxo de Caixa do Acionista"],
        "Valor2 (R$)": [lucro_liq,depreciacao,capex,var_capital_de_giro,fluxo_caixa_firma,fluxo_caixa_acionista]})

        st.table(fccaixa)

    with col17:

        ordem2 = [
            "Lucro Líquido",
            "(+) Depreciação",
            "(-) CAPEX",
            "(-) Δ Capital de Giro",
            "(=) Fluxo de Caixa da Firma",
        ]

        fccaixa = fccaixa.set_index("Item2").loc[ordem2].reset_index()

        items = fccaixa["Item2"].tolist()
        valores_plot = []

        # Tratamento correto dos valores para cascata
        for item, valor in zip(fccaixa["Item2"], fccaixa["Valor2 (R$)"]):
            if item in ["(+) Depreciação", "(-) CAPEX","(-) Δ Capital de Giro"]:
                valores_plot.append(-abs(valor))  # sempre descendente
            else:
                valores_plot.append(valor)

        measure = [
            "relative",  # Lucro Líquido
            "relative",  # Depreciação
            "relative",  # capex
            "relative",  # variação giro
            "total",     # Fluxo de caixa da firma
        ]


        fig2 = go.Figure(go.Waterfall(
            name="Fluxo de Caixa",
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

        
        fig2.update_layout(
            title="Fluxo de Caixa",
            showlegend=False,
            plot_bgcolor="#0F172A",
            paper_bgcolor="#0F172A",
            font=dict(color="#F1F5F9", family="Poppins"),
            xaxis=dict(tickangle=-15)
        )

        st.plotly_chart(fig2, use_container_width=True)

        # df_ffcaixa_grafico = fccaixa.set_index("Item2")[["Valor2 (R$)"]]
        #st.bar_chart(df_ffcaixa_grafico,sort = False)


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
                nopat = ebitda - depreciacao + (imposto)
                D_E = divida_bruta/patrimonio_liq
                st.metric("Debt/Equity",value = f"{D_E*100:.2f}%", delta="20%",)

            with col2:
                roe = divida_bruta/ebitda
                st.metric("Dívida/EBITDA",value = f"{roe*100:.2f}%", delta="20%",)

            with col1:
                roa = lucro_liq/ativo
                st.metric("ROA",value = f"{roa*100:.2f}%", delta="20%",)

with st.container(border = True):

    st.subheader("Modelo CAPM")

    
    
#primeira linha

    col1, col25, = st.columns(2,vertical_alignment = "top",width="stretch")
    

    with col1:
        

        st.write("Calculo do Beta",unsafe_allow_html=False)

        col1, col2 = st.columns(2,vertical_alignment = "top")

        with col1:

            periodos = {
            "6 meses": "6mo",
            "1 ano": "1y",
            "2 anos": "2y",
            "5 anos": "5y",
            "10 anos": "10y",
            }

            
            periodo_label = st.selectbox("Período de Cálculo",list(periodos.keys()))
            periodo = periodos[periodo_label]

            ticker_mercado_map = {
            "Ibovespa": "^BVSP",
            "SP500": "VOO",
            } 

            mercado = st.selectbox("Benchmark",list(ticker_mercado_map.keys()))
            ticker_mercado = ticker_mercado_map[mercado]

            def calcular_beta_setor(empresas, ticker_mercado= ticker_mercado, periodo=periodo):

                dados = yf.download(empresas + [ticker_mercado], period=periodo)["Close"]
                
                retornos = dados.pct_change().dropna()

                retorno_mercado = retornos[ticker_mercado]

                betas_individuais = {}

                # Calcular beta para cada empresa do setor
                for emp in empresas:
                    retorno_empresa = retornos[emp]
                    cov = np.cov(retorno_empresa, retorno_mercado)[0][1]
                    var = np.var(retorno_mercado)
                    beta = cov / var
                    betas_individuais[emp] = beta

                # Beta médio do setor (simples)
                beta_setor = np.mean(list(betas_individuais.values()))

                return beta_setor, betas_individuais
            

            setor = st.selectbox(
                "Selecione o setor",
                list(SETORES_EMPRESAS.keys())
                )
            

            if setor:
                empresas = SETORES_EMPRESAS[setor]
                beta_setor, betas_individuais = calcular_beta_setor(empresas,ticker_mercado=ticker_mercado,
                periodo=periodo)

            aliquota_pct = st.number_input("Aliquota para calculo do Beta Desalavancado, em %",min_value=0.0,
            max_value=100.0,value=34.0,step=0.1,format="%.1f")
            aliquota = aliquota_pct/100


            with col2:
                st.metric("Beta Médio Setorial", value=f"{beta_setor:.2f}")

                beta_desalavancado = beta_setor/(1+(1-aliquota)*D_E)  #calcular depois o D/E Médio do setor e alterar no código(é possível fazer com scrapping)
                
                st.metric("Beta Desalavancado", value=f"{beta_desalavancado:.2f}")

                beta_realavancado = beta_desalavancado*(1+(1-aliquota)*D_E)

                st.metric("Beta Realavancado", value=f"{beta_realavancado:.2f}")

    
    with col25:
            
            # --- Cálculo do retorno médio do setor (para o gráfico)
            dados_setor_grafico = yf.download(empresas, period=periodo)["Close"]
            retorno_setor = dados_setor_grafico.pct_change().dropna().mean(axis=1)

        
            # baixa preços do benchmark/mercado
            tabela2 = yf.download(ticker_mercado, period=periodo)["Close"]
            retorno_mercado = tabela2.pct_change().dropna()

            # concatena recebendo só as datas em comum
            tab_corr = pd.concat([retorno_setor, retorno_mercado], axis=1, join="inner")
            tab_corr.columns = ["Retorno Setor", "Retorno Mercado"]

            correlacao = px.scatter(
                tab_corr,
                x="Retorno Mercado",
                y="Retorno Setor",
                title="Retorno Setor vs Retorno Benchmark"
            )

            x = tab_corr["Retorno Mercado"]
            y = tab_corr["Retorno Setor"]
            coef = np.polyfit(x, y, 1) # regressão linear (y = ax + b)
            linha_tendencia = coef[0] * x + coef[1]

            correlacao_valor = np.corrcoef(x, y)[0, 1]
            r2 = correlacao_valor ** 2

            correlacao.add_scatter(
            x=x,
            y=linha_tendencia,
            mode="lines",
            name="Regressão Linear"
            )

            equacao_texto = f"y = {coef[0]:.3f}x + {coef[1]:.3f}<br>R² = {r2:.3f}"

            correlacao.add_annotation(
                x=0.05,
                y=0.95,
                xref="paper",
                yref="paper",
                text=equacao_texto,
                showarrow=False,
                font=dict(size=12, color="white"),
                bgcolor="rgba(0,0,0,0.5)",
                borderpad=6)


            correlacao.update_layout(
            plot_bgcolor="#0F172A", # área interna do gráfico
            paper_bgcolor="#0F172A" # área externa (margem)
            )
            st.plotly_chart(correlacao, use_container_width=True)

            # --- Evolução histórica do setor vs mercado ---

    with st.container(border = True):
                 
            # preços das empresas do setor
            dados_setor = yf.download(empresas, period=periodo)["Close"]

            # retorno médio do setor ao longo do tempo
            retorno_setor_diario = dados_setor.pct_change().dropna()
            retorno_setor_acumulado = (1 + retorno_setor_diario.mean(axis=1)).cumprod()

            # preços do benchmark
            dados_mercado = yf.download(ticker_mercado, period=periodo)["Close"]
            retorno_mercado_diario = dados_mercado.pct_change().dropna()
            retorno_mercado_acumulado = (1 + retorno_mercado_diario).cumprod()

            # juntar séries
            df_evolucao = pd.concat(
                [retorno_setor_acumulado, retorno_mercado_acumulado],
                axis=1,
                join="inner"
            )

            df_evolucao.columns = [setor, "Benchmark"]
            
            # gráfico de linha
            graf_evolucao = px.line(
                df_evolucao,
                title="Evolução: Setor vs Mercado",
                labels={"value": "Retorno Acumulado", "index": "Período"}
            )

            # fundo escuro (igual aos outros)
            graf_evolucao.update_layout(
                plot_bgcolor="#0F172A",
                paper_bgcolor="#0F172A",
                font_color="white")

            st.plotly_chart(graf_evolucao, use_container_width=True)
         


    with st.container(border = True):

        col1, col2 = st.columns(2,vertical_alignment = "top")
        
        with col1:
            st.subheader("CAPM - Cost of Equity (Ke)")
            with st.popover("Formula"):
                st.latex("CAPM =  Rf + β(Rm – Rf) + Rp")

            # Mostrar o resultado

            taxa_mercado = {
                "Ibovespa": "^BVSP",
                "SP500": "VOO",
            }

            col1, col3 = st.columns(2,vertical_alignment = "top")

            with col1:

                modelo_capm = st.selectbox(
                    "Modelo de CAPM",
                    ["Mercado (Atual)", "Damodaran (Histórico)"]
                )

                rf_opcao = st.selectbox(
                "Tipo de taxa livre de risco",
                [
                    "Tesouro Selic (Brasil)",
                    "Tesouro IPCA+ (Brasil)",
                    "US Treasury 10Y",
                    "US T-Bill 3M"
                ]
                )

                def obter_selic():
                    url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados/ultimos/1?formato=json"
                    resp = requests.get(url)
                    dados = resp.json()

                    selic = float(dados[0]["valor"]) / 100
                    return selic

                # Valores de exemplo (podemos automatizar depois)
                if rf_opcao == "Tesouro Selic (Brasil)":
                    rf = obter_selic()
                elif rf_opcao == "Tesouro IPCA+ (Brasil)":
                    rf = 0.060
                elif rf_opcao == "US Treasury 10Y":
                    rf = 0.1
                elif rf_opcao == "US T-Bill 3M":
                    rf = 0.053       

                # Selecionar mercado no Streamlit
                mercado_escolhido = st.selectbox("(RM) - Retorno de Mercado", list(taxa_mercado))

                # Obter ticker correspondente
                ticker_mercados= taxa_mercado[mercado_escolhido]

                # Baixar preços históricos do índice escolhido
                dados_mercado = yf.download(ticker_mercados, period=periodo)["Close"].dropna()

                # Função para calcular CAGR
                # Calcular CAGR
                preco_inicial = dados_mercado.iloc[0]
                preco_final = dados_mercado.iloc[-1]
                dias_totais = (dados_mercado.index[-1] - dados_mercado.index[0]).days
                anos = dias_totais / 365

                cagr_mercado = ((preco_final / preco_inicial) ** (1 / anos) - 1)*100
                cagr_valor = cagr_mercado.item()


            with col3:
                st.metric("Anos de Calculo",periodo)
                st.metric("Rf Taxa Livre de Risco",f"{rf:.2%}")
                st.metric(label="Rm - CAGR do Mercado", value=f"{cagr_valor:.2f}")

            with col1:
                risco_pais1 = st.number_input("Risco-País (em %)")
            with col3:
                capm1 = (rf + beta_realavancado*(cagr_valor - rf) + risco_pais1)/100
                st.metric("CAPM",f"{capm1:.2%}")
            
        with col2:

                st.subheader("Security Market Line (SML)")
                # --------------------------------------------------
                # Linha do gráfico (mantendo sua fórmula)
                # --------------------------------------------------
                betas = np.linspace(0, 2.5, 100)
                er = rf + betas * (cagr_valor - rf) + risco_pais1

                df1 = pd.DataFrame({
                    "Beta": betas,
                    "Retorno Esperado": er
                })

                # --------------------------------------------------
                # Ponto da empresa (mantendo suas variáveis)
                # --------------------------------------------------
                er_empresa = rf + beta_desalavancado * (cagr_valor - rf) + risco_pais1

                df_point = pd.DataFrame({
                    "Beta": [beta_desalavancado],
                    "Retorno Esperado": [er_empresa]
                })

                # --------------------------------------------------
                # Gráfico (MESMO PADRÃO do SML Damodaran)
                # --------------------------------------------------
                fig = px.line(
                    df1,
                    x="Beta",
                    y="Retorno Esperado",
                    title="Security Market Line (SML)",
                    labels={
                        "Beta": "Beta (β)",
                        "Retorno Esperado": "Retorno Esperado E(R)"
                    }
                )

                # Ponto do ativo
                fig.add_scatter(
                    x=df_point["Beta"],
                    y=df_point["Retorno Esperado"],
                    mode="markers",
                    marker=dict(size=14),
                    name="Empresa / Setor"
                )

                # --------------------------------------------------
                # Linha horizontal (Rf)
                # --------------------------------------------------
                fig.add_hline(
                    y=rf,
                    line_dash="dash",
                    annotation_text="Rf (Taxa Livre de Risco)",
                    annotation_position="bottom right",
                    line_color="white",
                )

                # --------------------------------------------------
                # Linha vertical (β = 1)
                # --------------------------------------------------
                fig.add_vline(
                    x=1,
                    line_dash="dash",
                    annotation_text="β = 1 (Mercado)",
                    annotation_position="top",
                    line_color="white",
                )

                # --------------------------------------------------
                # Layout
                # --------------------------------------------------
                fig.update_layout(
                    template="plotly_white",
                    hovermode="x unified",
                )

                fig.update_layout(
                plot_bgcolor="#0F172A",
                paper_bgcolor="#0F172A",
                font_color="white")

                st.plotly_chart(fig, use_container_width=True)


    with st.container(border = True): 
        st.subheader("CAPM - DAMODARAN - Mercado Emergentes")
        regiao = st.selectbox("Selecione a região",["US","Mercados Emergentes"])

        col1, col2,col3,col4,col5 = st.columns(5,vertical_alignment="top")
    
        df_damodaran = pd.read_excel("damodaran_data.xlsx")
        df_beta = pd.read_excel("damodaran_beta.xlsx")
        df_beta_us = pd.read_excel("damodaran_beta_us.xlsx")
        df_riscopais = pd.read_excel("damodaran_crp.xlsx")

        rm_damodaran = df_damodaran["S&P 500 (includes dividends)"].mean()
        rf_damodaran = df_damodaran["US T. Bond (10-year)"].mean()

        # Criar lista de setores
        setores = df_beta["Industry Name"].unique()
        paises = df_riscopais["Country"].unique()
        setores_us = df_beta_us["Industry Name"].unique()

        with col1:
                    
                    if regiao == "US":
                        setor = st.selectbox("Selecione o setor (US)", setores_us)
                        df_setor = df_beta_us[df_beta_us["Industry Name"] == setor].iloc[0]

                    else:
                        setor = st.selectbox("Selecione o setor (Mercados Emergentes)", setores)
                        df_setor = df_beta[df_beta["Industry Name"] == setor].iloc[0]

                    # Selectbox
                    #setor_escolhido = st.selectbox(
                        #"Selecione o setor (Damodaran)",
                        #setores
                    #)

                    # Filtrar a linha do setor escolhido
                    linha = df_beta[df_beta["Industry Name"] == setor].iloc[0]


                    # Extrair os valores
                    beta_damodaran = linha["Beta "]
                    de_ratio = linha["D/E Ratio"]
                    tax_rate = linha["Effective Tax rate"]
                    beta_unlevered = linha["Unlevered beta"]

                    linha2 = df_beta_us[df_beta_us["Industry Name"] == setor].iloc[0]

                    # Extrair os valores
                    beta_damodaran_us = linha2["Beta "]
                    de_ratio_us = linha2["D/E Ratio"]
                    tax_rate_us = linha2["Effective Tax rate"]
                    beta_unlevered_us = linha2["Unlevered beta"]

                    if regiao == "US":
                        st.metric("Beta (Damodaran)", f"{beta_damodaran_us:.2f}")
                    else:
                        st.metric("Beta (Damodaran)", f"{beta_damodaran:.2f}")
                
        with col2:  
                    if regiao == "US":               
                        st.metric("Taxa de Imposto", f"{tax_rate_us:.2%}")
                    else:
                        st.metric("Taxa de Imposto", f"{tax_rate:.2%}")
                    
                    if regiao == "US":
                        st.metric("Beta Desalavancado", f"{beta_unlevered_us:.2f}")
                    else:
                        st.metric("Beta Desalavancado", f"{beta_unlevered:.2f}")

        with col3:
                    if regiao == "US":
                        st.metric("D/E", f"{de_ratio_us:.2f}")
                    else:
                        st.metric("D/E", f"{de_ratio:.2f}") 
        with col4:
                    st.metric("D/E Empresa",f"{D_E:.2f}")
        with col5:
                    aliquota_emp = st.number_input("Imposto Empresa",min_value = 0.0, max_value = 1.0)
        with col3: 
                    if regiao == "US":
                        beta_realavancado_us = beta_unlevered_us *(1+(1-aliquota_emp)*D_E)
                        st.metric("Beta Realavancado",f"{beta_realavancado_us:.2f}")
                    else:
                        beta_realavancado = beta_unlevered *(1+(1-aliquota_emp)*D_E)
                        st.metric("Beta Realavancado",f"{beta_realavancado:.2f}")

                    df = pd.read_excel("damodaran_data.xlsx")
                    # Copiar só as colunas usadas e definir Year como índice
                    # Selecionar colunas e usar o Year como índice
                    df["S&P 500 (includes dividends)"] = df["S&P 500 (includes dividends)"] * 100
                    df["US T. Bond (10-year)"] = df["US T. Bond (10-year)"] * 100

        col1,col2,= st.columns(2)
        with col1:
            st.write("Calculando o CAPM")         
            st.latex("CAPM =  Rf + β(Rm – Rf) + Rp ")

        col1, col2,col3,col4,col5 = st.columns(5,vertical_alignment="top")

        with col1:
                
                pais_escolhido = st.selectbox(
                        "Selecione o País (Damodaran)",
                        paises
                    )
                    
                linha2 = df_riscopais[df_riscopais["Country"] == pais_escolhido].iloc[0]
                country_risco = linha2["CRP"]

        with col2:
                st.metric("Risco-Pais", f"{country_risco:.2%}")
        with col3:
                st.metric("Rm (Damodaran)", f"{rm_damodaran:.2%}")
        with col4:
                st.metric("Rf (Damodaran)", f"{rf_damodaran:.2%}")
        with col5:
                capm = rf_damodaran + beta_realavancado*(rm_damodaran - rf_damodaran) + country_risco
                st.metric("CAPM",f"{capm:.2%}")

        col1, col2 = st.columns(2,vertical_alignment="top")

        with col1:

            with st.container(border = False):
                # Criar o gráfico
                fig = px.line(
                    df,
                    x="Year",
                    y=["S&P 500 (includes dividends)", "US T. Bond (10-year)"],
                    title="Retornos Anuais - S&P 500 vs T-Bond 10Y",
                    labels={
                        "value": "Retorno (%)",
                        "variable": "Ativo"
                    }
                )

                # Deixar o layout parecido com Excel
                fig.update_traces(line=dict(width=2))
                fig.update_layout(
                    yaxis_tickformat=".1f",
                    xaxis_title="Ano",
                    yaxis_title="Retorno (%)",
                    legend_title_text=""
                )
                fig.update_layout(
                plot_bgcolor="#0F172A",
                paper_bgcolor="#0F172A",
                font_color="white")

                # Mostrar no Streamlit
                st.plotly_chart(fig, use_container_width=True)

        with col2:       

                betas = np.linspace(0, 2.5, 100)
                er = rf_damodaran + betas * (rm_damodaran - rf_damodaran)

                df = pd.DataFrame({
                    "Beta": betas,
                    "Retorno Esperado": er
                })

                # --------------------------------------------------
                # Ponto do setor/empresa
                # --------------------------------------------------
                er_empresa = rf_damodaran + beta_damodaran * (rm_damodaran - rf_damodaran)
                df_point = pd.DataFrame({
                    "Beta": [beta_damodaran],
                    "Retorno Esperado": [er_empresa]
                })

                # --------------------------------------------------
                # Criar gráfico com Plotly Express
                # --------------------------------------------------
                fig = px.line(
                    df,
                    x="Beta",
                    y="Retorno Esperado",
                    title="Security Market Line (SML)",
                    labels={"Beta": "Beta (β)", "Retorno Esperado": "Retorno Esperado E(R)"}
                )

                # Adicionar ponto do ativo/setor
                fig.add_scatter(
                    x=df_point["Beta"],
                    y=df_point["Retorno Esperado"],
                    mode="markers",
                    marker=dict(size=14),
                    name="Beta Damodaran"
                )

                # --------------------------------------------------
                # Linha horizontal (Rf)
                # --------------------------------------------------
                fig.add_hline(
                    y=rf_damodaran,
                    line_dash="dash",
                    annotation_text="Rf (Taxa Livre de Risco)",
                    annotation_position="bottom right",
                    line_color="white",
                )

                # --------------------------------------------------
                # Linha vertical em Beta = 1 (mercado)
                # --------------------------------------------------
                fig.add_vline(
                    x=1,
                    line_dash="dash",
                    annotation_text="β = 1 (Mercado)",
                    annotation_position="top",
                    line_color="white",
                )

                # --------------------------------------------------
                # Ajustes visuais
                # --------------------------------------------------
                fig.update_layout(
                    template="plotly_white",
                    hovermode="x unified",
                )

                fig.update_layout(
                plot_bgcolor="#0F172A",
                paper_bgcolor="#0F172A",
                font_color="white")

                # --------------------------------------------------
                # Mostrar no Streamlit
                # --------------------------------------------------
                st.plotly_chart(fig, use_container_width=True)

    with st.container(border = True): 
        st.subheader("CAPM - Adicione os seus valores")
        col1, col2 = st.columns(2)
        with col1:
                beta3= st.number_input("Beta")
                retorno_m = st.number_input("Rm Retorno mercado")
                taxa_li_risco = st.number_input("Rf taxa livre de risco")
                risco_paisss = st.number_input("Rp Risco pais")

                capm = (taxa_li_risco + beta3*(retorno_m-taxa_li_risco) + risco_paisss)/100
                st.metric("CAPM", f"{capm:.2%}" )

        with col2:
                betas5= np.linspace(0, 2.5, 100)
                er1 = taxa_li_risco + betas5 * (retorno_m - taxa_li_risco)

                df5 = pd.DataFrame({
                    "Beta": betas5,
                    "Retorno Esperado": er1
                })

                # --------------------------------------------------
                # Ponto do setor/empresa
                # --------------------------------------------------
                er_empresa5 = taxa_li_risco + beta3 * (retorno_m - taxa_li_risco)
                df_point1 = pd.DataFrame({
                    "Beta": [beta3],
                    "Retorno Esperado": [er_empresa5]
                })

                # --------------------------------------------------
                # Criar gráfico com Plotly Express
                # --------------------------------------------------
                fig = px.line(
                    df5,
                    x="Beta",
                    y="Retorno Esperado",
                    title="Security Market Line (SML)",
                    labels={"Beta": "Beta (β)", "Retorno Esperado": "Retorno Esperado E(R)"}
                )

                # Adicionar ponto do ativo/setor
                fig.add_scatter(
                    x=df_point1["Beta"],
                    y=df_point1["Retorno Esperado"],
                    mode="markers",
                    marker=dict(size=14),
                    name="Beta Damodaran"
                )

                # --------------------------------------------------
                # Linha horizontal (Rf)
                # --------------------------------------------------
                fig.add_hline(
                    y=taxa_li_risco,
                    line_dash="dash",
                    annotation_text="Rf (Taxa Livre de Risco)",
                    annotation_position="bottom right",
                    line_color="white",
                )

                # --------------------------------------------------
                # Linha vertical em Beta = 1 (mercado)
                # --------------------------------------------------
                fig.add_vline(
                    x=1,
                    line_dash="dash",
                    annotation_text="β = 1 (Mercado)",
                    annotation_position="top",
                    line_color="white",
                )

                # --------------------------------------------------
                # Ajustes visuais
                # --------------------------------------------------
                fig.update_layout(
                    template="plotly_white",
                    hovermode="x unified",
                )

                fig.update_layout(
                plot_bgcolor="#0F172A",
                paper_bgcolor="#0F172A",
                font_color="white")

                # --------------------------------------------------
                # Mostrar no Streamlit
                # --------------------------------------------------
                st.plotly_chart(fig, use_container_width=True)

    with st.container(border = True): 
        st.subheader("Kd - Custo de Terceiros")

        col1,col2 = st.columns(2)

        with col1:
            with st.container(border=True):
                st.write("Spread de Crédito + Taxa Livre de Riscos")
                st.latex("Spread + Taxa Livre de Riscos")

        with col2:
            with st.container(border=True):
                st.write("Kd Histórico")
                st.latex("Despesas Financeiras / Dívida Bruta")

        
        with st.container(border=True):
            st.write("Histórico de Empréstimos")
            
            meses = [
                "Valor","juros anuais", "juros mensais","Peso","Ponderada"]

            # Linhas (exemplo financeiro)

            linhas = ["Empréstimo 1", "Empréstimo 2", "Empréstimo 3","Empréstimo 4"]

            # DataFrame inicial
            df_inicial = pd.DataFrame(
                0.0,
                index=linhas,
                columns=meses
            )

            df_editado = st.data_editor(
            df_inicial,
            num_rows="dynamic"
            )

        
#beta ser selecionado por país e período ok 
#Adicionar no gráfico dos retornos - a porcentagem que eles valem
#para o beta dos eua, precisa ser usado as empresas do setor americano
#container de indicadores ok 
#container de wacc/capm
#container de multiplos
#container de Fleuriet
#Container de mensagem automatica com IA
# Gerar um pdf do arquivo
    
#Criar uma pagina chamada DFC, uma Taxa de Desconto e outra multiplos EBITDA elas servirão para explicar como foi feito o calculo do Valuation
#Qual os valores da participação da divida e equity, para minimizar o wacc e maximizar o ev da empresa
    

        
   



     



    