from fastapi.testclient import TestClient
from main import app
import numpy as np
import pandas as pd
import main

def ptax_falsa(*args, **kwargs):
    gerador = np.random.default_rng(42)
    valores = 5 + gerador.normal(0, 0.03, 60).cumsum()
    datas = pd.date_range("2026-08-01", periods=60, freq="B")
    return pd.DataFrame({"valor": valores}, index=datas)


cliente = TestClient(app)

def test_health_responde_200():
    resposta = cliente.get("/health")
    assert resposta.status_code == 200


def test_regime_retorna_campos_e_probabilidade_valida(monkeypatch):
    monkeypatch.setattr(main, "buscar_serie", lambda *a, **k: None)
    monkeypatch.setattr(main, "json_para_dataframe", ptax_falsa)

    resposta = cliente.get("/regime")
    corpo = resposta.json()

    assert resposta.status_code == 200
    assert set(corpo) == {"data", "prob_estresse", "regime"}
    assert 0 <= corpo["prob_estresse"] <= 1


def bcb_fora_do_ar(*args, **kwargs):
    raise ConnectionError("BCB fora do ar")

def test_url_indisponivel_retorna_503(monkeypatch):
    monkeypatch.setattr(main, "buscar_serie", bcb_fora_do_ar)
    resposta = cliente.get("/regime")
    assert resposta.status_code == 503