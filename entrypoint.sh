#!/bin/sh

echo "Waiting for postgres to start up..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 0.1
done
echo "PostgreSQL started"

exec "$@"