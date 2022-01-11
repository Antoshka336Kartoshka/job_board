#!/bin/bash

# Collect static files
echo "Collect static files"
python manage.py collectstatic --no-input

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate


gunicorn --bind :8000 --workers 3 job_board.wsgi:application