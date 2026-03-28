#!/bin/bash
set -e

python manage.py migrate --noinput
python manage.py compilemessages --ignore venv

python manage.py collectstatic --noinput

exec gunicorn config.wsgi:application \
  --workers 2 \
  --threads 2 \
  --worker-class gthread \
  --timeout 60 \
  --keep-alive 5 \
  --max-requests 1000 \
  --max-requests-jitter 100 \
  --bind 0.0.0.0:${PORT:-2000} \
  --log-level info
