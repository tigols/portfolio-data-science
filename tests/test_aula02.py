from src.aula02 import converter_valor, filtrar_vendas, venda_mais_cara
import pytest

vendas = [
    {"produto": "café", "valor": 12.0, "cidade": "SP"},
    {"produto": "pão", "valor": 5.5, "cidade": "RJ"},
    {"produto": "café", "valor": 12.0, "cidade": "RJ"},
]

@pytest.mark.parametrize("entrada, saida", 
                         [
                             ("0,50", 0.50),
                             ("10", 10.00)
                         ])
def test_texto_para_float(entrada, saida):
    assert converter_valor(entrada) == saida

@pytest.mark.parametrize("entrada",
                         [1, 2.5, None, ["10"]])
def test_texto_para_float_int(entrada):
    with pytest.raises(TypeError):
        converter_valor(entrada)

@pytest.mark.parametrize("vendas, cidade, valor_minimo, saida",
                         [(vendas, "RJ", 10, [{"produto": "café", "valor": 12.0, "cidade": "RJ"}])])
def test_filtrar_vendas(vendas, cidade, valor_minimo, saida):
    assert filtrar_vendas(vendas, cidade, valor_minimo) == saida

@pytest.mark.parametrize("entrada",
                         [1, "1", ["1"]])
def test_venda_mais_cara_int(entrada):
    with pytest.raises(TypeError):
        venda_mais_cara(entrada)