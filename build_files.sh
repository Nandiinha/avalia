#!/bin/bash
echo "Building the project..."
python3.9 -m pip install -r requirements.txt
python3.9 manage.py collectstatic --no-input
python3.9 manage.py migrate