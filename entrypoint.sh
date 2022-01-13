#!/bin/bash

# Collect static files
echo "Collect static files"
python manage.py collectstatic --no-input

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# Load default data
echo "Load default data"
python manage.py loaddata db.json


gunicorn --bind :8000 --workers 3 job_board.wsgi:application