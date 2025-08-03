#!/bin/sh

# Parámetros: host, puerto
host="db"
port=3306

echo "Esperando a MySQL en $host:$port..."

# Espera a que MySQL esté disponible
while ! nc -z $host $port; do
  sleep 1
done

echo "MySQL disponible! Ejecutando comando: $@"

# Ejecuta el comando original (python manage.py runserver ...)
exec "$@"
