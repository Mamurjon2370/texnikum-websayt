#!/bin/bash
# Vercel build bosqichi: `--break-system-packages` flagi bilan kutubxonalarni o'rnatish
python3.12 -m pip install -r requirements.txt --break-system-packages
python3.12 manage.py collectstatic --noinput --clear
