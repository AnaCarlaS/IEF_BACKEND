# Use uma imagem Python oficial
FROM python:3.11-slim

# Definir o diretório de trabalho
WORKDIR /usr/src/suporte

# Instalar dependências de sistema necessárias (GDAL, PROJ)
RUN apt-get update && apt-get install -y \
    binutils \
    libproj-dev \
    gdal-bin \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8030

CMD ["sh", "-c", "python manage.py migrate && \
                  python manage.py projeto_initial_data && \
                  gunicorn --workers 3 --preload --bind 0.0.0.0:8030 core.wsgi:application"]
# gunicorn --workers 3 --bind 0.0.0.0:8030 core.asgi:application -k uvicorn_worker.UvicornWorker
