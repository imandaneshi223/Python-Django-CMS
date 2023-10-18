#!/usr/bin/env bash
set -e
echo "[Django] collecting static files..."
python manage.py collectstatic --clear --noinput &>/dev/null
exec /root/.local/bin/gunicorn settings.wsgi:application \
     -w 2 \
     -b :8000
