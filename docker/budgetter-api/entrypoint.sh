#!/bin/bash
set -e

source /app/budgetter-api/.venv/bin/activate

python /app/budgetter-api/manage.py collectstatic --noinput
python /app/budgetter-api/manage.py migrate
python /app/budgetter-api/manage.py createsuperuser --noinput || true

exec apache2ctl -D FOREGROUND
