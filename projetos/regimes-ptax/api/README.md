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
   `curl "http://127.0.0.1:8000/regime?data_fim=2026-11-07"`

    Exemplo de resposta do `/regime`:
    `{ "data": "2026-11-06", "prob_estresse": 0.6168, "regime": "estresse"}`
5. Rode os testes (não dependem do BCB):
   `pytest -v`

## Como rodar com Docker

### 1. Instale o Docker
No Ubuntu, instale pelo terminal:

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

Permita usar o Docker sem `sudo`:

```bash
sudo usermod -aG docker $USER
```

Reinicie ou faça logout para aplicar. Depois, teste:

```bash
docker --version
docker run hello-world
```

### 2. Entenda os arquivos
O `Dockerfile` é a "receita" para gerar a imagem. A imagem é a receita congelada, resultado do `docker build`. O container é essa receita rodando.

Ao escrever um Dockerfile, imagine pegar um computador novo e adicionar só o que é necessário para rodar o seu script. Comece pelos passos mais estáveis, como a versão do Python e as dependências. No final ficam as partes que mudam com mais frequência, como o seu código e o comando que inicia a API. Assim o Docker reaproveita o cache dos passos de cima e o build fica mais rápido.

O `.dockerignore` funciona como um `.gitignore`: ele evita que arquivos como `.venv/` e `.git/` entrem na imagem.

### 3. Gere a imagem
A partir da raiz do repositório:

```bash
docker build -f projetos/regimes-ptax/api/Dockerfile -t api-ptax .
```

`-t` dá um nome (tag) à imagem. Sem ele, o Docker cria um ID aleatório, e você precisaria digitar esse ID sempre que quisesse subir a imagem. O `.` no final define o contexto do build: os arquivos da pasta onde o comando é executado. Os `COPY` do Dockerfile partem dessa pasta, por isso o build é rodado da raiz, onde fica a `src/`.

> O modelo é treinado durante o build, então é preciso estar com internet e com a API do BCB disponível.

### 4. Suba o container

```bash
docker run --rm -p 8000:8000 api-ptax
```

`-p 8000:8000` liga a porta 8000 do seu computador à porta 8000 do container. `--rm` remove o container quando ele é parado.

Acesse a documentação interativa em http://localhost:8000/docs