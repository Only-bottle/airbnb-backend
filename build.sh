#!/usr/bin/env bash
# exit on error
set -o errexit

pip install --upgrade pip
pip install poetry==1.2.0
rm poetry.lock
poetry lock
python -m poetry install
pip install --force-reinstall -U setuptools

python manage.py collectstatic --no-input
python manage.py migrate