import pandas as pd
import seaborn as sns


# Objetivo
# 1) Função exploratória de nulos
# 2) Função de taxa de sobrevivência agrupada

def resumo_nulos(df: pd.DataFrame):
    """
    Recebe um dataframe e devolve para cada coluna o percentual de nulos
    em ordem decrescente.
    """

    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"Deve ser passado um DataFrame, recebemos {type(df).__name__}")

    if df.empty:
        raise ValueError("O dataframe está vazio")

    percentual = (df.isna().sum() / df.shape[0]) * 100
    return percentual.sort_values(ascending=False)

def taxa_sobrevivencia_por(df: pd.DataFrame, grupo: str, alvo: str = "survived"):
    """
    Recebe um dataframe e retorna uma taxa da coluna alvo agrupado por um grupo
    """

    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"df precisa ser um pd.Dataframe, foi passado {type(df).__name__}")
    if not isinstance(grupo, str):
        raise TypeError(f"Grupo precisa ser str, foi passado grupo: {type(grupo).__name__}")
    if not isinstance(alvo, str):
            raise TypeError(f"Alvo precisa ser str, foi passado alvo: {type(alvo).__name__}")
    if df.empty:
        raise ValueError("O dataset está vazio.")
    if not all(nome in df.columns for nome in (alvo, grupo)):
        raise KeyError("O dataset não contém as colunas desejadas")
    if not df[alvo].dropna().isin([0, 1]).all():
        raise ValueError(f"A coluna alvo precisa conter apenas 0 e 1.")
    if df[alvo].dropna().empty:
        raise ValueError(f"Coluna alvo está vazia")

    # pegamos apenas as colunas de interesse para o calculo da taxa
    # tiramos os registros nulos, não assumimos nenhum valor para inputar (nesse caso usaria fillna())
    df_clean = df[[alvo, grupo]].dropna().copy()
    # como a coluna alvo é composta por 0 e 1, a taxa é a simples média da coluna, agrupada por grupo.
    taxas = df_clean.groupby(grupo)[alvo].mean()
    return taxas # retorna uma série


if __name__ == '__main__':
    dados = sns.load_dataset("titanic")

    print(resumo_nulos(dados))
    print(taxa_sobrevivencia_por(dados, grupo = "who"))
