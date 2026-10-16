# Aula 2
# Objetivo: funções bem escritas e tratamento de erros
# 1) converter_valor(texto), Teste "12,50" → 12.5, "12.50" → 12.5, e "abc" levantando ValueError.
# 2) filtrar_vendas(vendas, cidade=None, valor_minimo=0).
# 3) venda_mais_cara(vendas): devolve o dicionário da maior venda.

vendas = [
    {"produto": "café", "valor": 12.0, "cidade": "SP"},
    {"produto": "pão", "valor": 5.5, "cidade": "RJ"},
    {"produto": "café", "valor": 12.0, "cidade": "RJ"},
]


def converter_valor(texto: str) -> float:
    """Converte um valor em texto para float"""
    if not isinstance(texto, str):
        raise TypeError(f"A função deve receber um str, recebeu {type(texto).__name__}")

    try:
        return float(texto.replace(",", "."))
    except ValueError:
        raise ValueError(f"Valor inválido: {texto!r}")

def filtrar_vendas(vendas: list, cidade = None, valor_minimo = 0) -> list:
    """Filtra registro de uma lista de dicionarios por cidade e valor minimo"""
    resultado = [v for v in vendas if v['valor'] >= valor_minimo]
    for i, registro in enumerate(vendas):
        if not isinstance(registro, dict):
            raise TypeError(f"A lista deve conter dict, recebeu {type(registro).__name__}")
        if "cidade" not in registro:
            raise KeyError(f"Entrada {i} sem campo 'cidade': {registro}")
    
    if cidade is None:
        return resultado
    return [v for v in resultado if v['cidade'] == cidade]

def venda_mais_cara(vendas: list[dict]) -> dict:
    """retorna a venda mais cara"""
    if not vendas:
        raise ValueError("Lista não pode estar vazia")
    for registro in vendas:
        if not isinstance(registro, dict):
            raise TypeError(f"Lista deve conter dict, mas contém {type(registro).__name__} ")
    return max(vendas, key= lambda venda: venda['valor'])

if __name__ == "__main__":
    print(converter_valor("0,50"))
    print(filtrar_vendas(vendas=vendas, cidade = 'RJ', valor_minimo=10))
    print(venda_mais_cara(vendas))