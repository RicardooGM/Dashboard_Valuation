import streamlit as st

with open(".streamlit/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

with st.container(border=True):
    st.title("Taxa de Desconto")
    st.write("Página do Calculo da Taxa de Desconto")

st.subheader("O que é uma Taxa de Desconto e porque a calculamos?")
st.write("A Taxa de Desconto, no contexto de valuation, é a taxa usada para trazer"
" todos os fluxos de caixa futuros de uma empresa para o valor presente."
" Ela representa o retorno exigido pelo investidor para assumir o risco daquele investimento.")

st.subheader("Como ela é representada?")
st.write("Depende do método, mas geralmente:")

st.write("1. Para valuation do acionista (Fluxo de Caixa ao Acionista – FCA)")

st.write("👉 Usa-se o Custo do Patrimônio (Ke), normalmente calculado pelo CAPM.")

st.write("2. Para valuation da empresa (FCFF – Fluxo de Caixa Livre da Firma)")

st.write("👉 Usa-se o WACC (Custo Médio Ponderado de Capital), que combina:")

st.write("custo da dívida (Kd),")
st.write("custo do patrimônio (Ke),")
st.write("estrutura de capital (D/E).")

st.write("O WACC é a sigla para o termo em Inglês “Weighted Average Cost of Capital”" 
"que determina o custo conjunto do capital levantado por uma companhia"
"Esse capital pode advir de fontes internas, como os próprios acionistas ou de fontes externas, como os bancos."
"De qualquer forma, não é donativo e precisa retornar aos credores, que cobram juros pelo montante disponibilizado"
"Por isso, ele é considerado um custo e o WACC existe para mensurá-lo.")    

st.latex("WACC = Ke * E/D+E")
st.image("https://analystprep.com/cfa-level-1-exam/wp-content/uploads/2019/09/The-Security-Market-Line-SML.png")
st.image("https://media.wallstreetprep.com/uploads/2021/09/11224111/CAPM-Graph-960x638.jpg")
st.image("https://cienciaenegocios.com/wp-content/uploads/2016/10/CAPM_regressao.png")