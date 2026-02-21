#!/usr/bin/env bash
set -o errexit

set -o xtrace

echo "Upgrading pip.."
pip install --upgrade pip


echo "Installing dependencies..." 
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --no-input --clear

echo "Running migrations..."
python manage.py migrate

echo "Build completed successfully!"