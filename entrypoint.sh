#!/bin/bash
set -e

echo "=========================================="
echo " Iniciando configuración automática..."
echo "=========================================="

# =====================================================
# 1. GENERAR CLAVES RSA SI NO EXISTEN
# =====================================================
if [ ! -f "private_key.pem" ] || [ ! -f "public_key.pem" ]; then
    echo " Generando claves RSA..."
    python generar_rsa_keys.py
    echo " Claves RSA generadas correctamente"
else
    echo " Claves RSA ya existen"
fi

# =====================================================
# 2. GENERAR AES_SECRET_KEY SI NO EXISTE O ESTÁ VACÍA
# =====================================================
if [ -z "$AES_SECRET_KEY" ]; then
    echo " Generando AES_SECRET_KEY automáticamente..."
    export AES_SECRET_KEY=$(python -c "import os, base64; print(base64.urlsafe_b64encode(os.urandom(32)).decode())")
    echo " AES_SECRET_KEY generada: $AES_SECRET_KEY"
else
    echo " AES_SECRET_KEY ya está configurada"
fi

# =====================================================
# 3. ESPERAR A QUE MYSQL ESTÉ LISTO
# =====================================================
echo "⏳ Esperando a que MySQL esté listo..."
echo "   (Docker healthcheck se encarga de esto, esperando 10 segundos adicionales)"

# Esperar un poco extra después del healthcheck
sleep 10

echo "✅ Continuando con la configuración..."

# =====================================================
# 4. CREAR BASE DE DATOS SI NO EXISTE
# =====================================================
echo " Verificando base de datos..."

python << END
import MySQLdb

try:
    conn = MySQLdb.connect(
        host="${DB_HOST}",
        user="root",
        password="root",
        port=int("${DB_PORT}")
    )
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ejemplo_cifrado")
    conn.commit()
    cursor.close()
    conn.close()
    print(" Base de datos 'ejemplo_cifrado' lista")
except Exception as e:
    print(f"  Error al crear la base de datos: {e}")
END

# =====================================================
# 5. EJECUTAR MIGRACIONES
# =====================================================
echo " Ejecutando migraciones..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput
echo " Migraciones completadas"

# =====================================================
# 6. RECOLECTAR ARCHIVOS ESTÁTICOS
# =====================================================
echo " Recolectando archivos estáticos..."
python manage.py collectstatic --noinput || echo "  No se pudo recolectar archivos estáticos (puede ser normal)"

echo "=========================================="
echo " Configuración completada exitosamente"
echo " Iniciando servidor Django con Gunicorn..."
echo "=========================================="

# =====================================================
# 7. INICIAR GUNICORN
# =====================================================
exec gunicorn cifradoDatosReactDjango.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -
