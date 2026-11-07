import numpy as np
import pandas as pd
import statsmodels.api as sm
import joblib
import sys

sys.path.append("../../..")

from src.bcb import buscar_serie, json_para_dataframe, URL

# preparando dados
raw_data = buscar_serie(URL, "01/01/2016", "01/01/2026", timeout = 60)

df = json_para_dataframe(raw_data)
df['retorno'] = df['valor'].pct_change()*100

# Acredito que aqui nao precisamos fazer treino e teste pois o modelo ira direto nos dados de "teste" da vida real
# quando o usuário passar um dado do dia atual que está fora do periodo usado aqui para treinar o modelo


# treinando modelo
model_ptax = sm.tsa.MarkovRegression(df['retorno'].dropna(), k_regimes=2, trend='c', switching_variance=True)
model_ptax_fit = model_ptax.fit(maxiter=1000, disp=False, search_reps=20)

estresse = 1 if model_ptax_fit.params["sigma2[1]"] > model_ptax_fit.params["sigma2[0]"] else 0

final_model = {
    "estresse": estresse,
    "params": model_ptax_fit.params
}

joblib.dump(final_model, 'model_ptax.pkl')

