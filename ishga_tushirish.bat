@echo off
echo ====================================================
echo   2-son texnikumi sayti - ishga tushirish
echo ====================================================
if not exist venv (
  echo Virtual muhit yaratilmoqda...
  python -m venv venv
)
call venv\Scripts\activate
echo Kutubxonalar o'rnatilmoqda...
pip install -r requirements.txt
echo Ma'lumotlar bazasi tayyorlanmoqda...
python manage.py migrate
python manage.py seed
echo.
echo Server ishga tushmoqda: http://127.0.0.1:8000
echo Admin panel: http://127.0.0.1:8000/admin  (login: admin  parol: admin12345)
echo To'xtatish uchun: Ctrl+C
python manage.py runserver
