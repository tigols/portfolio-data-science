import pytest
import requests
from src.bcb import buscar_serie

class RespostaFalsa:
    def __init__(self, dados, status=200):
        self._dados = dados
        self.status_code = status
    def json(self):
        return self._dados

url = (
    "https://api.bcb.gov.br/dados/serie/bcdata.sgs.1/dados"
)
        
def test_retorna_dados(monkeypatch):
    falso = lambda *a, **k: RespostaFalsa([{'data': '02/01/2024', 'valor': '4.8916'}])
    monkeypatch.setattr(requests, "get", falso)
    assert buscar_serie(url, data_inicio='01/01/2024', data_fim='02/01/2024') == [{'data': '02/01/2024', 'valor': '4.8916'}]
def test_sem_internet(monkeypatch):
    def cai(*a, **k):
        raise requests.ConnectionError("rede caiu")
    monkeypatch.setattr(requests, "get", cai)
    with pytest.raises(ConnectionError, match = "Falha de rede"):
        buscar_serie(url, data_inicio='01/01/2024', data_fim='02/01/2024')
def test_timeout(monkeypatch):
    def timeout(*a, **k):
        raise requests.Timeout("timeout")
    monkeypatch.setattr(requests, "get", timeout)
    with pytest.raises(TimeoutError, match= "API demorou"):
        buscar_serie(url, data_inicio='01/01/2024', data_fim='02/01/2024')
def test_status(monkeypatch):
    falso = lambda *a, **k: RespostaFalsa([], status = 500)
    monkeypatch.setattr(requests, "get", falso)
    with pytest.raises(RuntimeError, match = "HTTP 500"):
        buscar_serie(url, data_inicio='01/01/2024', data_fim='02/01/2024')