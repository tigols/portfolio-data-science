## Como rodar a API

1. Instale as dependências (na raiz do repositório):
   `pip install -r requirements.txt`
2. Entre na pasta da API e treine o modelo (gera `model_ptax.pkl`):
   `cd projetos/regimes-ptax/api`
   `python treinar.py`
3. Suba a API (o `--reload` reinicia a API sozinho ao salvar o código):
   `uvicorn main:app --reload`
4. Teste pelo navegador em `http://127.0.0.1:8000/docs` (Swagger) ou pelo terminal:
   `curl http://127.0.0.1:8000/health`
   `curl "http://127.0.0.1:8000/regime?data_inicio=2026-09-01&data_fim=2026-11-06"`

Exemplo de resposta do `/regime`:
`{ "data": "2026-11-07", "prob_estresse": 0.6168, "regime": "estresse" }`
5. Rode os testes (não dependem do BCB):
   `pytest -v`