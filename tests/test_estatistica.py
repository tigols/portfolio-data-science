from src.aula00 import media, mediana

def test_media_simples():
    assert media([2, 4, 6]) == 4

def test_mediana_simples():
    assert mediana([3,1,2]) == 2