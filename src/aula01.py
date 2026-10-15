# Aula 1
# Objetivo: Trabalhar com dados estruturados como lista de dicionários
# mesmo formato que é usado em JSON e APIs
# Exercicios:
# 1) funcao total de vendas que soma os valores de vendas
# 2) funcao cidades unicas que retorna as cidades sem repeticao
# 3) funcao de vendas por produto 

vendas = [
    {"produto": "café", "valor": 12.0, "cidade": "SP"},
    {"produto": "pão", "valor": 5.5, "cidade": "RJ"},
    {"produto": "café", "valor": 12.0, "cidade": "RJ"},
]

def erro_lista_vazia():
    raise ValueError("A lista não pode estar vazia")

def total_vendas(vendas: list) -> float:
    """Soma valores do item "valor" de uma lista de dicionarios"""
    if not vendas:
        erro_lista_vazia()
    return sum(item["valor"] for item in vendas)


def cidades_unicas(vendas: list) -> set:
    """Retorna um set de cidades dado uma lista de dicionarios"""
    if not vendas:
        erro_lista_vazia()
    return set(item["cidade"] for item in vendas)

def vendas_por_produto(vendas: list) -> dict:
    """Retorna o total da soma de valor para cada produto em uma lista de dicionarios"""
    if not vendas:
        erro_lista_vazia()
                             
    totais = {}
    for item in vendas:
        produto = item["produto"]
        totais[produto] = totais.get(produto, 0) + item['valor']

    return totais


if __name__ == "__main__":
    print(total_vendas(vendas))
    print(cidades_unicas(vendas))
    print(vendas_por_produto(vendas))
