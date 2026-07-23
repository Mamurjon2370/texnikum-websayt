# O'zbekiston tuman 2-son texnikumi — veb-sayt

Django asosidagi to'liq veb-sayt: ma'lumot beruvchi sahifalar + o'rnatilgan **admin panel** orqali boshqariladigan kontent (yo'nalishlar, yangiliklar, onlayn arizalar, xodimlar, galereya, hujjatlar, FAQ).

## Imkoniyatlar

- **Bosh sahifa** — hero, statistika, yo'nalishlar, biz haqimizda, so'nggi yangiliklar
- **Biz haqimizda** — tarix, rahbariyat, o'qituvchilar, meyoriy hujjatlar
- **Yo'nalishlar** — 11 ta mutaxassislik, har biri uchun batafsil sahifa (muddat, diplom, grant/kontrakt)
- **Qabul** — onlayn ariza shakli + kerakli hujjatlar + FAQ
- **Yangiliklar** — ro'yxat, qidiruv, sahifalash, batafsil ko'rinish
- **Galereya** — fotogalereya
- **Aloqa** — murojaat shakli + Google xarita
- **Qidiruv** — sayt bo'ylab qidirish
- **Admin panel** — barcha kontentni boshqarish (`/admin`)
- Mobil qurilmalarga moslashgan (responsive), 3 tilga tayyor tuzilma (UZ/RU/EN)

## Ishga tushirish (Windows)

Eng oson yo'l — `ishga_tushirish.bat` faylini ikki marta bosing. U hamma narsani avtomatik bajaradi.

Yoki qo'lda:

```bat
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed
python manage.py runserver
```

So'ng brauzerda oching: **http://127.0.0.1:8000**

## Admin panel

- Manzil: **http://127.0.0.1:8000/admin**
- Login: `admin`
- Parol: `admin12345`

> ⚠️ Ishlab chiqarishga (real serverga) qo'yishdan oldin parolni albatta o'zgartiring:
> `python manage.py changepassword admin`

Admin paneldan yo'nalishlar, yangiliklar, xodimlar, galereya rasmlari, hujjatlar qo'shasiz; kelgan arizalar va murojaatlarni ko'rasiz; sayt sozlamalarini (nom, logotip, telefon, ijtimoiy tarmoqlar, xarita) tahrirlaysiz.

## `seed` buyrug'i

`python manage.py seed` — texnikum javoblari asosida boshlang'ich ma'lumotlarni (yo'nalishlar, namunaviy yangiliklar, FAQ, sozlamalar) va admin foydalanuvchini yaratadi. Bir necha marta ishga tushirsa ham ma'lumotni takrorlamaydi.

## Loyiha tuzilishi

```
texnikum-websayt/
├── manage.py
├── requirements.txt
├── ishga_tushirish.bat
├── texnikum/          # loyiha sozlamalari (settings, urls)
├── core/              # asosiy app (modellar, viewlar, admin, formalar)
│   ├── models.py
│   ├── views.py
│   ├── admin.py
│   ├── forms.py
│   └── management/commands/seed.py
├── templates/         # HTML shablonlar
├── static/css/        # dizayn (style.css)
└── media/             # yuklangan rasm/hujjatlar
```

## Kelgusi qadamlar (rejadagi imkoniyatlar)

Javoblarda ko'rsatilgan quyidagilar keyingi bosqichda qo'shilishi mumkin:
domen va hosting sozlash, SSL (https), talaba/o'qituvchi shaxsiy kabineti, Hemis bilan integratsiya, to'liq UZ/RU/EN tarjimalari, zaxira nusxa (backup) tizimi, tashriflar statistikasi.

## Texnologiyalar

Python · Django 5 · SQLite · Bootstrap 5 · Bootstrap Icons
