from fastapi import FastAPI, Query
import datetime as dt
import joblib
import statsmodels.api as sm
import sys
sys.path.append("../../..")
from src.bcb import buscar_serie, json_para_dataframe, URL

app = FastAPI()

modelo = joblib.load('model_ptax.pkl')


@app.get("/health")
def verificar_saude():
    return {"status": "ok"}

@app.get("/regime")
def buscar_regime(
    data_inicio: dt.date | None = Query(None, description="Data Inicial (AAAA-MM-DD)", examples=["2026-09-01"]), 
    data_fim: dt.date | None = Query(None, description="Data Final (AAAA-MM-DD)", examples=["2026-10-06"])
    ):
    """Busca o regime de volatilidade para a data alvo"""
    if not data_fim:
        data_fim = dt.date.today()
    if not data_inicio:
        data_inicio = data_fim - dt.timedelta(days=60)


    dados_ptax = buscar_serie(URL, data_fim=data_fim.strftime("%d/%m/%Y"), data_inicio=data_inicio.strftime("%d/%m/%Y"), timeout= 60)
    dados_ptax = json_para_dataframe(dados_ptax)
    retornos = dados_ptax['valor'].pct_change().dropna()*100

    modelo_novo = sm.tsa.MarkovRegression(retornos, k_regimes=2, trend='c', switching_variance=True)

    params = modelo['params'][modelo_novo.param_names]
    res = modelo_novo.filter(params)

    prob_estresse = res.filtered_marginal_probabilities.iloc[-1, modelo["estresse"]]

    return {
            "data": data_fim.isoformat(),
            "prob_estresse": round(float(prob_estresse), 4),
            "regime": "estresse" if prob_estresse > 0.5 else "normal",
        }
