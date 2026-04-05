# 1. Imagen base ligera (slim) para mantener el peso bajo
FROM python:3.12-slim

# 2. Instalamos uv en el contenedor copiándolo directamente desde su imagen oficial
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 3. Definimos el directorio de trabajo dentro del contenedor
WORKDIR /app

# 4. Copiamos PRIMERO los archivos de configuración de dependencias.
# Esto optimiza el caché de Docker: si modificas main.py, Docker no volverá a descargar todo.
COPY pyproject.toml uv.lock ./

# 5. Instalamos las dependencias. 
# --frozen asegura que instale exactamente las versiones del lockfile.
RUN uv sync --frozen --no-cache

# 6. Copiamos el resto de nuestro código (main.py y test_main.py)
COPY . .

# 7. Exponemos el puerto que pide la rúbrica
EXPOSE 8000

# 8. Comando para ejecutar el servidor de FastAPI a través de uv
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]