# abertura, funcao de media em python
def media(numeros: list):
    """Retorna a média aritmética de uma lista de números."""
    if not numeros:
        raise ValueError("A lista não pode estar vazia.")
    return sum(numeros) / len(numeros)


def mediana(numeros: list):
    """Retorna a mediana de uma lista de números"""
    if not numeros:
        raise ValueError("A lista não pode estar vazia.")

    ordenados = sorted(numeros)
    n = len(ordenados)
    meio = n // 2
    if n % 2 == 0:
        return (ordenados[meio - 1] + ordenados[meio]) / 2
    return ordenados[meio]
