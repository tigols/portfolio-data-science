import pytest
import pandas as pd
from src.titanic import resumo_nulos, taxa_sobrevivencia_por

df_taxa = pd.DataFrame({"ativo": [0,1,0,1],
                        "modelo": ["pequeno", "medio", "medio", "grande"],
                        })

df_taxa_nulo = pd.DataFrame({"ativo": [pd.NA,pd.NA,pd.NA,pd.NA],
                        "modelo": ["pequeno", "medio", "medio", "grande"],
                        })

df_vazio = pd.DataFrame()

df = pd.DataFrame({
    "cidade": ["SP", "RJ", None, "SP"],
    "populacao": [12.0, None, None, 12.0],
})

esperado = pd.Series({"populacao": 50.0, "cidade": 25.0})

taxa_esperada = pd.Series([1,0.5,0], index = pd.Index(["grande", "medio", "pequeno"], name= "modelo"), name = "ativo")
# podemos nomear a série e os indices, para nomear a série passe name= por fora e para indice passe dentro do pd.Index()
# podemos contornar o erro de nomes divergentes tirando a checagem de names dentro do pd.testing.assert_series_equal(check_names=False)

taxa_esperada_2 = pd.DataFrame({
    "modelo": ["grande", "medio", "pequeno"],
    "media": [1, 0.5, 0],
    "n": [1,2,1]
})


@pytest.mark.parametrize("entrada",
                         [(df_vazio)])
def test_resumo_nulos_df_vazio(entrada):
    with pytest.raises(ValueError):
        resumo_nulos(entrada)

@pytest.mark.parametrize("entrada",
                         [(), "abc", 1])
def test_resumo_nulos_tipo_errado(entrada):
    with pytest.raises(TypeError):
        resumo_nulos(entrada)

def test_resumo_nulos():
    pd.testing.assert_series_equal(resumo_nulos(df), esperado)


@pytest.mark.parametrize("dataset, grupo, alvo",
                         [
                             (pd.DataFrame(), "modelo", "ativo")
                         ])
def test_taxa_df_vazio(dataset, grupo, alvo):
    with pytest.raises(ValueError):
        taxa_sobrevivencia_por(dataset, grupo, alvo)

@pytest.mark.parametrize("dataset, grupo, alvo",
                         [
                             (df_taxa_nulo, "modelo", "ativo")
                         ])
def test_taxa_alvo_todo_nulo(dataset, grupo, alvo):
    with pytest.raises(ValueError):
        taxa_sobrevivencia_por(dataset, grupo, alvo)


@pytest.mark.parametrize("dataset, grupo, alvo",
                        [
                            (df_taxa, "teste", "ativo"),
                            (df_taxa, "modelo", "teste")
                        ])
def test_taxa_coluna_inexistente(dataset, grupo, alvo):
    with pytest.raises(KeyError):
        taxa_sobrevivencia_por(dataset, grupo, alvo)

@pytest.mark.parametrize("dataset, grupo, alvo",
                        [
                            (pd.Series([1,2]), "modelo", "ativo"),
                            (df_taxa, 1, 2),
                            (df_taxa, ["modelo"], "ativo"),
                            (df_taxa, "modelo", 0),
                        ])
def test_taxa_tipo_invalido(dataset, grupo, alvo):
    with pytest.raises(TypeError):
        taxa_sobrevivencia_por(dataset, grupo, alvo)



@pytest.mark.parametrize("dataset, grupo, alvo",
                        [
                            (df_taxa, "modelo", "ativo"),
                        ])
def test_taxa_por_grupo(dataset, grupo, alvo):
    pd.testing.assert_frame_equal(taxa_sobrevivencia_por(dataset, grupo, alvo), taxa_esperada_2)