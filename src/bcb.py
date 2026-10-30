########################################################################
##
##              Puxar dados da API do Banco central
##
########################################################################

import requests

# Mapa Mental
# 1) Passar a URL de endpoint
# 2) Definir funcao de busca

URL = (
    "https://api.bcb.gov.br/dados/serie/bcdata.sgs.1/dados"
) # duas strings uma ao lado da outra, ou com espaco ou quebra de linha sao coladas automaticamente
# essa URL vira uma coisa só, o () permite a quebra de linha

def buscar_serie(url: str, data_inicio: str = '01/01/2024', data_fim: str = '31/03/2024', timeout: float = 10)-> list:
    """Busca JSON na API do BCB. Falha alto se a rede ou o servidor falhar"""

    params = {"dataInicial": data_inicio, "dataFinal": data_fim}

    # Utilizamos "try" para chamar, se falhar damos raise com "except"
    try:
        resp = requests.get(url, params=params, timeout= timeout)
    except requests.Timeout as e:
        raise TimeoutError(f"API demorou mais que {timeout}s: {url}") from e
    except requests.RequestException as e:
        raise ConnectionError(f"Falha de rede ao chamar {url}") from e

    if resp.status_code != 200:
        raise RuntimeError(
            f"API respondeu HTTP {resp.status_code}, não são dados vazios."
        )

    dados = resp.json()

    if not isinstance(dados, list):
        raise ValueError("JSON inesperado: esperava uma lista.")

    return dados

########################################################################
##
##              Transformar JSON em DataFrame
##
########################################################################

import pandas as pd

def json_para_dataframe(serie: list) -> pd.DataFrame:
    """Recebe uma lista JSON e transforma em DataFrame"""
    if not serie:
        raise ValueError("Série está vazia")
    if not isinstance(serie, list):
        raise TypeError(f"A série deve ser uma lista, não {type(serie)}")

    df = pd.DataFrame(serie)

    if not {"data", "valor"}.issubset(df.columns): # se data e valor nao forem um conjunto das colunas do df
        raise KeyError("JSON sem colunas 'data' e 'valor'.")

    df['data'] = pd.to_datetime(df['data'], dayfirst=True) # dayfirst = True pois na serie do BCB vem com formato dd/MM/yyyy
    df['valor'] = pd.to_numeric(df['valor'], errors='raise')
    return df.sort_values('data').reset_index(drop = True) # devolve o df ordenado por data e remove a coluna de index

########################################################################
##
##              Criar tabela no Banco de Dados
##
########################################################################

import os
import psycopg


# DDL = Data Definition Language
# Temos DML = Data Manipulation Language que mexe nos dados (abaixo)
DDL = """
    CREATE TABLE IF NOT EXISTS bcb_usd_ptax (
        data DATE PRIMARY KEY,
        valor NUMERIC NOT NULL
    );
"""

# UPSERT = UPDATE + INSERT > insere dados mas se a chave ja existe atualiza
# %s são da biblioteca psycopg e são placeholders
# Nesse caso passamos (data, valor) no executemany() e a lib coloca valores com escape seguro o que previne SQL Injection
# Dois %s = duas colunas
# ON CONFLICT (data): se já existir linha com essa data (PRIMARY KEY), não quebra com erro de duplicata.
# DO UPDATE SET valor = EXCLUDED.valor: atualiza o valor com o da linha que você tentou inserir. EXCLUDED é o nome que o Postgres dá à linha “nova” que perdeu o conflito.
UPSERT = """
    INSERT INTO bcb_usd_ptax (data, valor)
    VALUES (%s, %s)
    ON CONFLICT (data) DO UPDATE SET valor = EXCLUDED.valor;
"""
# Ao final, se rodar duas vezes o pipeline, nao duplicamos linhas, apenas atualiza o valor do dia se ele mudou

def salvar_postgres(df: pd.DataFrame) -> int:
    # Assim como fazia no trabalho para subir as tabelas no databricks
    # Passamos os valores da conexão e depois usamos cursor()
    conninfo = (
        f"host={os.environ['PGHOST']} port={os.environ['PGPORT']} "
        f"dbname={os.environ['PGDATABASE']} user={os.environ['PGUSER']} "
        f"password={os.environ['PGPASSWORD']}"
    )

    with psycopg.connect(conninfo) as conn:
        with conn.cursor() as cur:
            cur.execute(DDL)
            rows = [
                (row.data.date(), float(row.valor))
                for row in df.itertuples(index=False)
            ]
            cur.executemany(UPSERT, rows)
        conn.commit()
    return len(rows)


if __name__ == "__main__":
    serie = buscar_serie(URL, data_inicio='01/01/2024', data_fim='31/12/2024')
    print(len(serie), serie[0]) # esta devolvendo corretamente 22 registros  sendo o primeiro dia 2 de janeiro de 2024
    # note que JSON é uma lista de dicionarios

    df = json_para_dataframe(serie)

    print(df.head())
    print(df.dtypes)

    n = salvar_postgres(df)
    print(f"gravou {n} linhas")
