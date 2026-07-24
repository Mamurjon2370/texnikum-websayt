#!/bin/bash
# Vercel build bosqichi: kutubxonalarni o'rnatadi va statik fayllarni to'playdi.
pip install -r requirements.txt
python3.12 manage.py collectstatic --noinput --clear
