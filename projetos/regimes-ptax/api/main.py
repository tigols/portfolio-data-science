from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def verificar_saude():
    return {"status": "ok"}