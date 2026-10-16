# Portfólio de Data Science

Registro da minha jornada aprendendo Python, boas práticas de código e ciência de dados, do básico até projetos aplicados.

## Objetivo
Construir fluência em Python escrevendo o código eu mesmo e aplicar conceitos de ciência de dados em problemas reais.

## Estrutura
- `src/`: funções reutilizáveis
- `tests/`: testes automatizados com pytest
- `notebooks/`: análises e experimentos
- `data/`: dados (os brutos não vão para o Git)

## Progresso
| Aula | Tema | Status |
|------|------|--------|
| 00 | Ambiente, funções de média e mediana, testes | ✅ |
| 01 | Listas, dicionários e comprehensions | ✅ |

## Como rodar
```
python -m venv .venv
.venv\Scripts\activate
pip install pytest
python -m pytest
```

## Aprendizados
- Erros devem lançar exceções, não retornar texto.
- `/` sempre devolve float; para índices, use `//`.
- O nome de um teste deve dizer o que ele testa.
- Para somar por categoria, acumule num dicionário com dict.get(chave, 0).
- if __name__ == "__main__" evita que o código rode quando o arquivo é só importado.
