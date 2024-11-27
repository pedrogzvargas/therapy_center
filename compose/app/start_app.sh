#!/bin/sh

set -o errexit
set -o nounset

echo "================================================================================================================="
echo "Start app"
echo "================================================================================================================="

alembic upgrade head
gunicorn --bind 0.0.0.0:5000 wsgi:app