FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/
COPY projetos/regimes-ptax/api/ projetos/regimes-ptax/api/

RUN python projetos/regimes-ptax/api/treinar.py

EXPOSE 8000

CMD ["uvicorn", "main:app", "--app-dir", "projetos/regimes-ptax/api", "--host", "0.0.0.0", "--port", "8000"]