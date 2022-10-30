#!/usr/bin/env bash
# exit on error
set -o errexit

#para generar requirements.txt
#pip freeze > requirements.txt

# poetry install
pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate