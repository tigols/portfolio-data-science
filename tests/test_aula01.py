from src.aula01 import total_vendas, cidades_unicas, vendas_por_produto
import pytest

vendas = [
    {"produto": "café", "valor": 12.0, "cidade": "SP"},
    {"produto": "pão", "valor": 5.5, "cidade": "RJ"},
    {"produto": "café", "valor": 12.0, "cidade": "RJ"},
]

def test_total_vendas():
    assert  total_vendas(vendas) == 29.5

def test_total_vendas_lista_vazia():
    with pytest.raises(ValueError):
        total_vendas([])

def test_cidades_unicas():
    assert cidades_unicas(vendas) == {'SP', 'RJ'}

def test_cidades_unicas_lista_vazia():
    with pytest.raises(ValueError):
        cidades_unicas([])

def test_vendas_por_produto():
    assert vendas_por_produto(vendas) == {'café': 24.0, 'pão': 5.5}

def test_vendas_por_produto_lista_vazia():
    with pytest.raises(ValueError):
        vendas_por_produto([])