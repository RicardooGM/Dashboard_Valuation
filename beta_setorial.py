import yfinance as yf
import numpy as np

def calcular_beta_setor(empresas, ticker_mercado="^BVSP", periodo="2y"):
    
    dados = yf.download(empresas + [ticker_mercado], period=periodo)["Close"]
    
    retornos = dados.pct_change().dropna()

    retorno_mercado = retornos[ticker_mercado]
    retorno_setor = retornos[empresas].mean(axis=1)

    cov = np.cov(retorno_setor, retorno_mercado)[0][1]
    var = np.var(retorno_mercado)

    beta = cov / var
    return beta



