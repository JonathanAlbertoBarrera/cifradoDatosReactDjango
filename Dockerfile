# Dockerfile para Django Backend
FROM python:3.11-slim

# Variables de entorno para Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema necesarias para mysqlclient y cryptography
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    gcc \
    g++ \
    libssl-dev \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Actualizar pip y instalar wheel
RUN pip install --upgrade pip setuptools wheel

# Copiar requirements e instalar dependencias Python
COPY requirements.txt .

# Instalar mysqlclient primero (es el más problemático)
RUN pip install --no-cache-dir mysqlclient==2.2.8

# Luego instalar el resto de dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código del proyecto
COPY . .

# Dar permisos de ejecución al entrypoint
RUN chmod +x /app/entrypoint.sh

# Exponer puerto 8000
EXPOSE 8000

# Usar entrypoint para configuración automática
ENTRYPOINT ["/app/entrypoint.sh"]
