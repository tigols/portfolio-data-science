import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from src.titanic import resumo_nulos, taxa_sobrevivencia_por
import pandas as pd
import numpy as np


# Variable	Definition	Key
# survival	Survival	0 = No, 1 = Yes
# pclass	Ticket class	1 = 1st, 2 = 2nd, 3 = 3rd
# sex	Sex	
# Age	Age in years	
# sibsp	# of siblings / spouses aboard the Titanic	
# parch	# of parents / children aboard the Titanic	
# ticket	Ticket number	
# fare	Passenger fare	
# cabin	Cabin number	
# embarked	Port of Embarkation	C = Cherbourg, Q = Queenstown, S = Southampton



# Objetivo
# 1) Visualização das variáveis
# 2) Montar uma visualização minha de uma informação que quero mostrar



## ===================================================================
## 1) Quanto falta de dado e onde?
## ===================================================================
def preparar_nulos(df: pd.DataFrame) -> pd.DataFrame:
    """Devolve as colunas com nulos (variavel, percentual), da maior para a menor."""
    df_nulos = resumo_nulos(df).reset_index()
    df_nulos.columns = ['variavel', 'percentual']
    return df_nulos[df_nulos['percentual'] > 0]


def plot_valores_faltantes(df: pd.DataFrame, caminho: str = "reports/figs/titanic/01_percentual_de_nulos.png"):
    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"O dataset deve ser do tipo pd.DataFrame e recebemos {type(df).__name__}")

    if df.empty:
        raise ValueError("O dataset está vazio")

    df_nulos = preparar_nulos(df)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=df_nulos, x='variavel', y='percentual', ax=ax)
    for barras in ax.containers:
        ax.bar_label(barras, fmt="%.2f%%", label_type="center")
    ax.set_ylim(0, 100)
    ax.set_title("Percentual de valores faltantes por variável")
    ax.set_xlabel("Variável")
    ax.set_ylabel("Percentual de Nulos")
    fig.tight_layout()
    Path(caminho).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(caminho, dpi=150)
    plt.close(fig)
    return fig


## ===================================================================
# 2) Quem estava abordo?
## ===================================================================
def plot_grupos_a_bordo(df: pd.DataFrame):

    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"O dataset deve ser do tipo pd.DataFrame e recebemos {type(df).__name__}")

    if df.empty:
        raise ValueError("O dataset está vazio")
    for _ in ['class']:
        if _ not in df.columns:
            raise KeyError(f"{_} não está entre as colunas do dataframe")


    fig, ax = plt.subplots(figsize = (10,6))
    sns.barplot(data = df, x = "class", y = "count",
                hue = "sex", ax = ax)
    for barra in ax.containers:
         ax.bar_label(barra, label_type="edge")
    fig.savefig("reports/figs/titanic/02_grupos_a_bordo.png")
    plt.show()
    plt.close(fig)

def plot_idades_por_grupo(df: pd.DataFrame):
    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"O dataset deve ser do tipo pd.DataFrame e recebemos {type(df).__name__}")

    if df.empty:
        raise ValueError("O dataset está vazio")
    for _ in ['sex', 'class', 'age']:
        if _ not in df.columns:
            raise KeyError(f"{_} não está entre as colunas do dataframe")

    g = sns.displot(data = df, x = "age", col = "class", row = "sex", facet_kws=dict(margin_titles = True),
                binwidth = 3, height= 3)
    g.figure.savefig("reports/figs/titanic/03_idades_por_grupo.png")
    plt.show()
    plt.close(g.figure)


## ===================================================================
# 3) Taxa de sobrevivência por sexo? E por idade?
## ===================================================================

def plot_sobrevivencia(df:pd.DataFrame, grupo: str):
    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"O dataset deve ser do tipo pd.DataFrame e recebemos {type(df).__name__}")
    if not isinstance(grupo, str):
        raise TypeError(f"Grupo deve ser do tipo str, recebemos {type(grupo).__name__}")

    if df.empty:
        raise ValueError("O dataset está vazio")
    for _ in [grupo]:
        if _ not in df.columns:
            raise KeyError(f"{_} não está entre as colunas do dataframe")
        

    df_sobrevivencia = taxa_sobrevivencia_por(df, grupo)
    df_sobrevivencia["media"] = df_sobrevivencia["media"] * 100

    fig, ax = plt.subplots(figsize = (10,6))
    sns.barplot(df_sobrevivencia, x = grupo, y = 'media', ax = ax)
    textos = [f"{m:.1f}%\n(n={n})" for m, n in zip(df_sobrevivencia["media"], df_sobrevivencia["n"])]
    for bar in ax.containers:
        ax.bar_label(bar, labels=textos, label_type='center')


    ax.set_title(f"Taxa de sobrevivência por {grupo}")
    ax.set_ylabel("Percentual de Sobreviventes")
    fig.savefig(f"reports/figs/titanic/04_sobrevivencia_por_{grupo}.png")
    plt.show()


if __name__ == '__main__':
    dados = sns.load_dataset("titanic")
    condicoes = [
        dados['age'] <= 25,
        (dados['age'] > 25) & (dados['age'] <= 50),
        (dados['age'] > 50) & (dados['age'] <= 75),
        dados['age'] > 75
    ]
    faixas = ["0-25", "26-50", "51-75", "75+"]
    dados['age_bucket'] = np.select(condicoes, faixas, default="Unknown")


    df_sex_class = dados[['sex', 'class']].value_counts().reset_index().sort_values("sex")
    df_sex_class_age = dados[['sex', 'class', 'age']].sort_values("sex")
    plot_valores_faltantes(dados)
    plot_grupos_a_bordo(df_sex_class)
    plot_idades_por_grupo(df_sex_class_age)
    plot_sobrevivencia(dados, "sex")
    plot_sobrevivencia(dados, "age_bucket")


    
