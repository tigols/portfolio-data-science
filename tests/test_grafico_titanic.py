import matplotlib
matplotlib.use("Agg")  # backend sem janela: o pytest nao pode abrir figuras

import pandas as pd
import pytest

from src.graficos_titanic import (
    plot_sobrevivencia,
    plot_valores_faltantes,
    preparar_nulos,
)

df_exemplo = pd.DataFrame({
    "var1": [pd.NA, pd.NA, pd.NA, pd.NA],   # 100% nulos
    "var2": [pd.NA, 1, 2, 3],               # 25% nulos
    "var3": ["A", "B", "C", "D"],           # 0% nulos
})


# ===== preparar_nulos: o que o grafico vai desenhar =====

def test_preparar_nulos_mantem_so_colunas_com_nulos():
    esperado = pd.DataFrame({"variavel": ["var1", "var2"],
                             "percentual": [100.0, 25.0]})
    pd.testing.assert_frame_equal(preparar_nulos(df_exemplo), esperado)


# ===== plot_valores_faltantes =====

def test_plot_valores_faltantes_cria_arquivo(tmp_path):
    caminho = tmp_path / "nulos.png"
    plot_valores_faltantes(df_exemplo, caminho)
    assert caminho.exists()


def test_plot_valores_faltantes_df_vazio():
    with pytest.raises(ValueError):
        plot_valores_faltantes(pd.DataFrame())


@pytest.mark.parametrize("entrada", [pd.Series([1, 2]), "abc", 1])
def test_plot_valores_faltantes_tipo_errado(entrada):
    with pytest.raises(TypeError):
        plot_valores_faltantes(entrada)


# ===== plot_sobrevivencia =====

def test_plot_sobrevivencia_coluna_inexistente():
    df = pd.DataFrame({"survived": [0, 1], "sex": ["male", "female"]})
    with pytest.raises(KeyError):
        plot_sobrevivencia(df, "coluna_que_nao_existe")
