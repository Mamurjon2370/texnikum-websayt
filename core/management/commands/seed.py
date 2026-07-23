from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.utils import timezone
from django.contrib.auth import get_user_model
from core.models import SiteSettings, Program, News, NewsCategory, Staff, FAQ

PROGRAMS = [
    ("Moda va tikuv ishlab chiqarish texnologiyasi", "scissors"),
    ("Oshpaz", "egg-fried"),
    ("Bino va inshootlarni pardozlash ustasi", "bricks"),
    ("Metallga qayta ishlov berish", "gear"),
    ("Kompyuter tarmoqlari va IT-servis", "hdd-network"),
    ("Traktor va agrotexnikalar mashinisti", "truck"),
    ("Laborant ekolog", "droplet"),
    ("Avtomobillar servisi", "car-front"),
    ("Turar joy infratuzilmasi servisi", "house-gear"),
    ("Dasturiy injiniring", "code-slash"),
    ("Buxgalteriya va audit", "calculator"),
]

FAQS = [
    ("Qabul qanday amalga oshiriladi?", "Qabul o'quvchining arizasiga muvofiq amalga oshiriladi."),
    ("Qanday hujjatlar kerak?", "O'quvchi shaxsini tasdiqlovchi metrika yoki pasport, ota-ona pasporti va 3x4 rasm."),
    ("O'qish muddati qancha?", "Barcha yo'nalishlarda o'qish muddati 2 yil."),
    ("O'qish qaysi tilda olib boriladi?", "O'qish o'zbek tilida olib boriladi."),
    ("Amaliyot qayerda o'tkaziladi?", "Amaliyot tumandagi hamkor tashkilotlarda o'taladi."),
    ("Grant o'rinlari bormi?", "Ha, davlat granti asosida o'qish imkoniyati mavjud."),
]

NEWS = [
    ("2026-2027 o'quv yili uchun qabul boshlandi",
     "Texnikumimizga yangi o'quv yili uchun hujjat qabuli boshlandi. Onlayn ariza topshirish imkoniyati mavjud."),
    ("Talabalarimiz hamkor korxonalarda amaliyot o'tashmoqda",
     "O'quvchilarimiz tumandagi hamkor tashkilotlarda kasbiy amaliyot o'tab, real ish tajribasiga ega bo'lmoqda."),
    ("Xalqaro hamkorlik doirasida yangi loyihalar",
     "Texnikum xalqaro hamkorlarni jalb qilish va ta'lim sifatini oshirish bo'yicha yangi loyihalarni boshladi."),
]


class Command(BaseCommand):
    help = "Boshlang'ich ma'lumotlarni yuklaydi"

    def handle(self, *args, **opts):
        s = SiteSettings.get()
        s.about_short = ("O'zbekiston tuman 2-son texnikumi 1973-yilda tashkil etilgan bo'lib, "
                         "o'rta bo'g'in malakali kadrlarni tayyorlashga ixtisoslashgan kasb-hunar "
                         "ta'limi muassasasidir. Texnikum Oliy ta'lim, fan va innovatsiyalar vazirligi "
                         "huzuridagi Kasbiy ta'lim agentligiga qaraydi.")
        s.telegram = "https://t.me/"
        s.instagram = "https://instagram.com/"
        s.save()
        self.stdout.write("Sayt sozlamalari yangilandi.")

        for i, (title, icon) in enumerate(PROGRAMS):
            Program.objects.update_or_create(
                slug=slugify(title),
                defaults=dict(
                    title=title, icon=icon, order=i, duration="2 yil",
                    diploma="Boshlang'ich professional ta'lim", language="O'zbek tili",
                    grant_places=9, contract_places=11, contract_price="4 635 000",
                    description=f"{title} yo'nalishi bo'yicha malakali mutaxassislar tayyorlanadi. "
                                f"Nazariy bilimlar amaliy ko'nikmalar bilan uyg'unlashtiriladi.",
                ))
        self.stdout.write(f"{len(PROGRAMS)} ta yo'nalish qo'shildi.")

        cat, _ = NewsCategory.objects.get_or_create(slug="umumiy", defaults={"name": "Umumiy"})
        for i, (t, b) in enumerate(NEWS):
            News.objects.update_or_create(
                slug=slugify(t)[:60] or f"news-{i}",
                defaults=dict(title=t, body=b, summary=b[:120], category=cat,
                              published_at=timezone.now(), is_published=True))
        self.stdout.write(f"{len(NEWS)} ta yangilik qo'shildi.")

        for i, (q, a) in enumerate(FAQS):
            FAQ.objects.update_or_create(question=q, defaults={"answer": a, "order": i})
        self.stdout.write(f"{len(FAQS)} ta FAQ qo'shildi.")

        Staff.objects.get_or_create(full_name="Texnikum direktori", defaults=dict(
            position="Direktor", role="management", order=0))
        Staff.objects.get_or_create(full_name="J. Nabijonov", defaults=dict(
            position="Maxsus fan o'qituvchisi", role="teacher", order=0))
        self.stdout.write("Rahbariyat qo'shildi.")

        User = get_user_model()
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "uzbekistandistrict2ps@gmail.com", "admin12345")
            self.stdout.write("Admin yaratildi: admin / admin12345")
        self.stdout.write(self.style.SUCCESS("Tayyor!"))
